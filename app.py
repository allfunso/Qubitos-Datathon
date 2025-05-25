import json
import pandas as pd

# Load JSON files
with open('costos.json', 'r') as f:
    costos = json.load(f)

with open('tasas_banco_metodo.json', 'r') as f:
    tasas = json.load(f)

def calcular_potencial(banco, emisora, monto, metodo="default"):
    try:
        tasa = tasas[banco][emisora]
        costo = costos[banco][metodo]
        expected_value = tasa * monto
        return expected_value, expected_value > costo
    except KeyError:
        return None, None

def modo_interactivo():
    banco = input("Nombre del banco: ").strip().upper()
    print(tasas[banco].keys())
    emisora = input("Emisora: ").strip().upper()
    monto = float(input("Monto a cobrar: "))

    expected, potencial = calcular_potencial(banco, emisora, monto)

    if expected is None:
        print("⚠️ Datos no encontrados en los archivos JSON.")
    else:
        print(f"\n✅ Valor esperado: ${expected:.2f}")
        print("🔍 Tiene potencial: " + ("✅ Sí" if potencial else "❌ No"))

def modo_archivo():
    file_path = input("Ruta al archivo CSV: ").strip()
    output_path = input("Ruta para guardar el archivo con 'potencial' (por defecto: output.csv): ").strip() or "output.csv"

    df = pd.read_csv(file_path)

    def evaluar_fila(row):
        monto = row['montoCobrar']
        emisora_info = row['nombreEmisora'].split(maxsplit=1)
        if len(emisora_info) < 2:
            emisora_info = [row['nombreBanco'], 'default']
        banco, emisora = emisora_info
        metodo = "default"

        try:
            costo = costos[banco][metodo]
            tasa = tasas[banco][emisora]
            expected_value = tasa * monto
            return expected_value > costo
        except KeyError:
            # If no matching cost found, return None or False
            return None

    df['potencial'] = df.apply(evaluar_fila, axis=1)
    df.to_csv(output_path, index=False)
    print(f"✅ Archivo guardado en: {output_path}")

def main():
    print("=== Evaluador de Órdenes de Cobro ===")
    print("1. Modo interactivo")
    print("2. Modo archivo")
    choice = input("Selecciona una opción (1 o 2): ").strip()

    if choice == '1':
        modo_interactivo()
    elif choice == '2':
        modo_archivo()
    else:
        print("❌ Opción inválida.")

if __name__ == "__main__":
    main()