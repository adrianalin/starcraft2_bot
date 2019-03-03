import sc2
from sc2 import position, Result, UnitTypeId
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, CYBERNETICSCORE, STALKER, STARGATE, VOIDRAY, \
    OBSERVER, ROBOTICSFACILITY, FLEETBEACON, CARRIER
import random
import numpy as np
import cv2
import time
import math


class BotTest(sc2.BotAI):

    def __init__(self):
        super(BotTest, self).__init__()

        self.do_something_after = 0
        self.train_data = []

        self.max_nexuses = 4
        self.max_stargetes = 6
        self.game_time = 0
        self.unit_types = list()
        self.choices = {0: self.do_nothing,
                        1: self.unit_closest_nexus,
                        2: self.enemy_structures,
                        3: self.enemy_start
                        }
        self.current_choice = 0

    def on_end(self, game_result):
        print('--- on_end called ---')
        print(game_result)

        if game_result == Result.Victory:
            np.save("train_data/{}.npy".format(str(int(time.time()))), np.array(self.train_data))

    async def on_step(self, iteration: int):
        self.game_time = (self.state.game_loop / 22.4) / 60
        await self.scout()
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()
        await self.offensive_force_buildings()
        await self.build_offensive_force()
        await self.attack_something()
        await self.intel()

    def random_location_variance(self, enemy_start_location):
        x = enemy_start_location[0]
        y = enemy_start_location[1]

        x += ((random.randrange(-20, 20)) / 100) * self.game_info.map_size[0]
        y += ((random.randrange(-20, 20)) / 100) * self.game_info.map_size[1]

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.game_info.map_size[0]:
            x = self.game_info.map_size[0]
        if y > self.game_info.map_size[1]:
            y = self.game_info.map_size[1]

        go_to = position.Point2(position.Pointlike((x, y)))
        return go_to

    async def scout(self):
        if len(self.units(OBSERVER)) > 0:
            scout = self.units(OBSERVER)[0]
            if scout.is_idle:
                enemy_location = self.enemy_start_locations[0]
                move_to = self.random_location_variance(enemy_location)
                await self.do(scout.move(move_to))

        else:
            if self.units(ROBOTICSFACILITY).ready.exists:
                for rf in self.units(ROBOTICSFACILITY).ready.noqueue:
                    if self.can_afford(OBSERVER) and self.supply_left > 0:
                        await self.do(rf.train(OBSERVER))

    async def intel(self):
        game_data = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)

        for unit in self.units().ready:
            pos = unit.position
            cv2.circle(game_data, (int(pos[0]), int(pos[1])), int(unit.radius * 8), (255, 255, 255),
                       math.ceil(int(unit.radius * 0.5)))

        for unit in self.known_enemy_units:
            pos = unit.position
            cv2.circle(game_data, (int(pos[0]), int(pos[1])), int(unit.radius * 8), (125, 125, 125),
                       math.ceil(int(unit.radius * 0.5)))

        try:
            line_max = 50
            mineral_ratio = self.minerals / 1500
            if mineral_ratio > 1.0:
                mineral_ratio = 1.0

            vespene_ratio = self.vespene / 1500
            if vespene_ratio > 1.0:
                vespene_ratio = 1.0

            population_ratio = self.supply_left / self.supply_cap
            if population_ratio > 1.0:
                population_ratio = 1.0

            plausible_supply = self.supply_cap / 200.0

            worker_weight = len(self.units(PROBE)) / (self.supply_cap - self.supply_left)
            if worker_weight > 1.0:
                worker_weight = 1.0

            cv2.line(game_data, (0, 19), (int(line_max*worker_weight), 19), (250, 250, 200), 3)  # worker/supply ratio
            cv2.line(game_data, (0, 15), (int(line_max*plausible_supply), 15), (220, 200, 200), 3)  # plausible supply (supply/200.0)
            cv2.line(game_data, (0, 11), (int(line_max*population_ratio), 11), (150, 150, 150), 3)  # population ratio (supply_left/supply)
            cv2.line(game_data, (0, 7), (int(line_max*vespene_ratio), 7), (210, 200, 0), 3)  # gas / 1500
            cv2.line(game_data, (0, 3), (int(line_max*mineral_ratio), 3), (0, 255, 25), 3)  # minerals minerals/1500
        except Exception as e:
            print(str(e))

        # flip horizontally to make our final fix in visual representation:
        self.flipped = cv2.flip(game_data, 0)
        # resized = cv2.resize(self.flipped, dsize=None, fx=2, fy=2)

        # cv2.imshow('Intel', self.flipped)
        cv2.waitKey(1)

    async def attack_something(self):
        if len(self.units(VOIDRAY).idle) > 0 and len(self.units(CARRIER).idle) > 0:

            if self.game_time > self.do_something_after:
                self.current_choice = random.randrange(0, len(self.choices))
                print(self.current_choice)
                target = self.choices[self.current_choice]()
                await self.do_attack(target)

            y = np.zeros(len(self.choices))
            y[self.current_choice] = 1
            self.train_data.append([y, self.flipped])

    async def do_attack(self, target):
        if len(self.units(CARRIER)) > 1 and len(self.units(VOIDRAY)) > 1:
            for car in self.units(CARRIER):
                await self.do(car.attack(target))
            for vr in self.units(VOIDRAY):
                await self.do(vr.attack(target))

    def do_nothing(self):
        wait = random.randrange(7, 100)/100
        self.do_something_after = self.game_time + wait
        return None

    def unit_closest_nexus(self):
        if len(self.known_enemy_units) > 0 and self.units(NEXUS).exists:
            target = self.known_enemy_units.closest_to(random.choice(self.units(NEXUS)))
            return target

    def enemy_structures(self):
        if len(self.known_enemy_structures) > 0:
            if len(self.known_enemy_structures) > 0:
                target = random.choice(self.known_enemy_structures)
        return target

    def enemy_start(self):
        target = self.enemy_start_locations[0]
        return target

    async def on_unit_destroyed(self, unit_tag):
        target = self.unit_closest_nexus()
        self.current_choice = 1
        await self.do_attack(target)

    async def build_offensive_force(self):
        for sg in self.units(STARGATE).ready.noqueue:
            if self.units(FLEETBEACON).ready:
                if self.can_afford(CARRIER) and self.supply_left > 0:
                    await self.do(sg.train(CARRIER))
            if self.can_afford(VOIDRAY) and self.supply_left > 0:
                await self.do(sg.train(VOIDRAY))

    async def offensive_force_buildings(self):
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random
            if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon.position.towards(self.game_info.map_center, 5))

            elif len(self.units(GATEWAY)) < 1:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon.position.towards(self.game_info.map_center, 5))

            if self.units(CYBERNETICSCORE).ready.exists:
                if len(self.units(ROBOTICSFACILITY)) < 1:
                    if self.can_afford(ROBOTICSFACILITY) and not self.already_pending(ROBOTICSFACILITY):
                        await self.build(ROBOTICSFACILITY, near=pylon.position.towards(self.game_info.map_center, 5))

            if self.units(CYBERNETICSCORE).ready.exists:
                if len(self.units(STARGATE)) < self.max_stargetes:
                    if self.can_afford(STARGATE) and not self.already_pending(STARGATE):
                        await self.build(STARGATE, near=pylon.position.towards(self.game_info.map_center, 5))

            if self.units(STARGATE).ready.exists:
                if len(self.units(FLEETBEACON)) < 1:
                    if self.can_afford(FLEETBEACON) and not self.already_pending(FLEETBEACON):
                        await self.build(FLEETBEACON, near=pylon.position.towards(self.game_info.map_center, 5))

    async def expand(self):
        if self.units(NEXUS).amount < self.max_nexuses \
                and self.can_afford(NEXUS) \
                and not self.already_pending(NEXUS):
            await self.expand_now()

    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(10.0, nexus)
            for vaspene in vaspenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(ASSIMILATOR, vaspene))

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=self.units(NEXUS).first.position.towards(self.game_info.map_center, 5))


    async def build_workers(self):
        if len(self.units(NEXUS)) * 16 > len(self.units(PROBE)) - 1:
            for nexus in self.units(NEXUS).ready.noqueue:
                if self.can_afford(PROBE):
                    await self.do(nexus.train(PROBE))

    def stop_game(self):
        print('stop game')
        pass

    def units_effective(self):
        unit_types = {UnitTypeId[unit.name.upper()] for unit in self.units()}
        for unit in (unit_types - set(self.unit_types)):
            self.unit_types.append(unit)

        return [(unit, len(self.units(unit).ready), len(self.units(unit).not_ready))
                for unit in self.unit_types]

    def set_max_nexuses(self, count):
        self.max_nexuses = count

    def set_max_stargates(self, count):
        self.max_stargetes = count

    def attack_choice(self):
        return str(self.current_choice)
