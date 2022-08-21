from dataclasses import dataclass
from typing import ClassVar

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    
    def get_message(self) -> None:
        return (f'''Тип тренировки: {self.training_type};
                Длительность: {round(self.duration, 3)} ч.;
                Дистанция: {round(self.distance, 3)} км.;
                Ср. скорость: {round(self.speed, 3)} км/ч;
                Потрачено ккал.: {round(self.calories, 3)}.''')
        


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight


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
        pass
        

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
    coeff_calorie_1: ClassVar[int] = 18
    coeff_calorie_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 
                * self.get_mean_speed()
                - self.coeff_calorie_2)
                * self.weight
                / self.M_IN_KM
                * self.duration) 
    


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_1: ClassVar[float] = 0.035
    coeff_2: ClassVar[int] = 2
    coeff_3: ClassVar[float] = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        return ((self.coeff_1
                * self.weight
                + (self.get_mean_speed()
                    ** self.coeff_2
                    // self.height)
                * self.coeff_3
                * self.weight)
                * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float]= 1.38
    coeff_1:  ClassVar[float] = 1.1
    coeff_2:  ClassVar[ int ] = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_poll: int):
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_poll = count_poll
    def get_mean_speed(self) -> float:
        return (self.lenght_pool
                * self.count_poll
                / Training.M_IN_KM
                / self.duration)
                
    def get_distance(self) -> float:
        distance = (self.action
                    * Swimming.LEN_STEP 
                    / Training.M_IN_KM)
        return distance

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                    + self.coeff_1)    
                * self.coeff_2
                * self.weight)

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    parameters_train = {
        'SWM' : Swimming,
        'RUN' : Running,
        'WLK' : SportsWalking}
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

