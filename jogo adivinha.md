import java.util.Random;
import java.util.Scanner;

public class JogoAdivinhacao {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();
        int numeroAleatorio = random.nextInt(100) + 1; // Gera um número aleatório entre 1 e 100
        int tentativas = 0;
        int palpite;

        System.out.println("Bem-vindo ao Jogo de Adivinhação!");
        System.out.println("Tente adivinhar o número secreto entre 1 e 100.");

        do {
            System.out.print("Digite seu palpite: ");
            palpite = scanner.nextInt();
            tentativas++;

            if (palpite < numeroAleatorio) {
                System.out.println("Tente um número maior.");
            } else if (palpite > numeroAleatorio) {
                System.out.println("Tente um número menor.");
            }
        } while (palpite != numeroAleatorio);

        System.out.println("Parabéns! Você acertou o número em " + tentativas + " tentativas.");
        scanner.close();
    }
}
