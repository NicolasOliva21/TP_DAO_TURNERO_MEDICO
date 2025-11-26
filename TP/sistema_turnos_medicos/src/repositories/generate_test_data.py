"""
Script para generar datos de prueba masivos para el sistema.
Genera pacientes adicionales, turnos históricos y futuros, y consultas médicas.
"""
import random
from datetime import datetime, timedelta, time
from src.repositories.unit_of_work import UnitOfWork
from src.repositories.init_data import inicializar_datos_base
from src.domain.paciente import Paciente
from src.domain.turno import Turno
from src.domain.consulta import Consulta

def generar_pacientes_extra(uow: UnitOfWork, cantidad: int = 10):
    """Genera pacientes adicionales."""
    nombres = ["Ana", "Luis", "Marta", "Jorge", "Elena", "Pedro", "Sofia", "Diego", "Lucia", "Pablo"]
    apellidos = ["Garcia", "Martinez", "Lopez", "Sanchez", "Rodriguez", "Fernandez", "Gomez", "Diaz", "Perez", "Romero"]
    
    print(f"[GEN] Generando {cantidad} pacientes extra...")
    
    for i in range(cantidad):
        dni = f"{random.randint(10000000, 99999999)}"
        if uow.pacientes.get_by_dni(dni):
            continue
            
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        
        paciente = Paciente(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            email=f"{nombre.lower()}.{apellido.lower()}{i}@example.com",
            telefono=f"261-{random.randint(4000000, 9999999)}",
            fecha_nacimiento=datetime(random.randint(1960, 2005), random.randint(1, 12), random.randint(1, 28)).date(),
            direccion=f"Calle Falsa {random.randint(100, 999)}",
            obra_social=random.choice(["OSDE", "Swiss Medical", "Osecac", None])
        )
        uow.pacientes.add(paciente)
    
    uow.flush()

def generar_turnos_masivos(uow: UnitOfWork):
    """Genera turnos pasados y futuros para todos los médicos."""
    medicos = uow.medicos.get_all()
    pacientes = uow.pacientes.get_all()
    estados = {
        "PEND": uow.estados_turno.get_by_codigo("PEND"),
        "CONF": uow.estados_turno.get_by_codigo("CONF"),
        "ASIS": uow.estados_turno.get_by_codigo("ASIS"),
        "CANC": uow.estados_turno.get_by_codigo("CANC"),
        "INAS": uow.estados_turno.get_by_codigo("INAS"),
    }
    
    if not medicos or not pacientes:
        print("[GEN] Error: Faltan médicos o pacientes base.")
        return

    print(f"[GEN] Generando turnos para {len(medicos)} médicos...")

    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for medico in medicos:
        # Turnos pasados (últimos 30 días)
        for _ in range(20):
            dias_atras = random.randint(1, 30)
            fecha = hoy - timedelta(days=dias_atras)
            hora = time(random.randint(9, 17), random.choice([0, 30]))
            fecha_hora = datetime.combine(fecha, hora)
            
            # Estado aleatorio para pasados (ASIS, INAS, CANC)
            estado_codigo = random.choices(["ASIS", "INAS", "CANC"], weights=[0.7, 0.2, 0.1])[0]
            estado = estados[estado_codigo]
            
            paciente = random.choice(pacientes)
            especialidad = random.choice(medico.especialidades)
            
            turno = Turno(
                id_paciente=paciente.id,
                id_medico=medico.id,
                id_especialidad=especialidad.id,
                fecha_hora=fecha_hora,
                duracion_minutos=30,
                id_estado=estado.id,
                observaciones="Consulta general"
            )
            uow.turnos.add(turno)
            uow.flush()
            
            # Si asistió, crear consulta
            if estado_codigo == "ASIS":
                consulta = Consulta(
                    id_turno=turno.id,
                    motivo="Dolor de cabeza y fiebre",
                    diagnostico="Gripe estacional",
                    indicaciones="Reposo y paracetamol",
                    fecha_atencion=fecha_hora + timedelta(minutes=15)
                )
                uow.consultas.add(consulta)

        # Turnos futuros (próximos 30 días)
        for _ in range(10):
            dias_adelante = random.randint(1, 30)
            fecha = hoy + timedelta(days=dias_adelante)
            hora = time(random.randint(9, 17), random.choice([0, 30]))
            fecha_hora = datetime.combine(fecha, hora)
            
            # Estado aleatorio para futuros (PEND, CONF)
            estado_codigo = random.choice(["PEND", "CONF"])
            estado = estados[estado_codigo]
            
            paciente = random.choice(pacientes)
            especialidad = random.choice(medico.especialidades)
            
            turno = Turno(
                id_paciente=paciente.id,
                id_medico=medico.id,
                id_especialidad=especialidad.id,
                fecha_hora=fecha_hora,
                duracion_minutos=30,
                id_estado=estado.id,
                observaciones="Control anual"
            )
            uow.turnos.add(turno)

if __name__ == "__main__":
    from src.repositories.database import db_manager
    
    print("="*60)
    print("GENERADOR DE DATOS DE PRUEBA")
    print("="*60)
    
    # Asegurar que la BD existe y tiene datos base
    db_manager.initialize()
    db_manager.create_tables()
    inicializar_datos_base()
    
    with UnitOfWork() as uow:
        try:
            generar_pacientes_extra(uow)
            generar_turnos_masivos(uow)
            uow.commit()
            print("\n[SUCCESS] Datos generados exitosamente.")
        except Exception as e:
            print(f"\n[ERROR] {e}")
            uow.rollback()
