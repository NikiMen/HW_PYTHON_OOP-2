from dataclasses import dataclass
from typing import ClassVar, Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    HH_IN_MM: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action
                * self.LEN_STEP
                / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в %s.' % self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar[int] = 18
    COEFF_CALORIE_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight
                / self.M_IN_KM
                * (self.duration * self.HH_IN_MM))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1: ClassVar[float] = 0.035
    COEFF_2: ClassVar[float] = 0.029
    COEFF_3: ClassVar[int] = 2
    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return ((self.COEFF_1
                * self.weight
                + (self.get_mean_speed()
                    ** self.COEFF_3
                    // self.height)
                * self.COEFF_2
                * self.weight)
                * (self.duration * self.HH_IN_MM))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_1: ClassVar[float] = 1.1
    MATH_DEGREE: ClassVar[int] = 2
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / Training.M_IN_KM
                / self.duration)

    def get_distance(self) -> float:
        distance = (self.action
                    * self.LEN_STEP
                    / Training.M_IN_KM)
        return distance

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.COEFF_1)
                * self.MATH_DEGREE
                * self.weight)


def read_package(workout_type: Dict[str, str], data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    parameters_train = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in parameters_train:
        return parameters_train[workout_type](*data)
    else:
        raise ValueError('Тренировка не найдена')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
