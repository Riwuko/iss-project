from .base_tuner_model import TunerModel


class ZieglerNicholsTunerModel(TunerModel):
    """Ziegler Nichols PID Tunning Method """
    class Meta:
        slug = "Ziegler-Nichols"
        

    def add_tuning(self, tu, P=None, I=None, D=None, error=0, delta_error=0, delta_time=0):
        """
        Metoda do obliczania nowych wartości P, I, D zgodnie z algorytmem tuningu; 
        w tej chwili przyjmuje i oblicza dokładnie to samo co regulator bez tuningu, żeby cokolwiek się działo.
        W konsoli serwera printuje że się wykonała xD 
        """
        P_computed = P * error
        I_computed = I * error * delta_time
        D_computed = 0.0
        if delta_time > 0:
            D_computed = D * delta_error / delta_time
        
        print(f"Tunning done with {self.Meta.slug} tuner")
        return P_computed, I_computed, D_computed

