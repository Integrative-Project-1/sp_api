"""Cálculo de progreso por actividad (subtareas hechas / total)."""


def activity_progress(*, done: int, total: int) -> dict:
    """Retorna conteo y porcentaje redondeado (misma regla que el frontend)."""
    if total == 0:
        return {'subtasks_done': 0, 'subtasks_total': 0, 'progress_percent': 0}
    return {
        'subtasks_done': done,
        'subtasks_total': total,
        'progress_percent': round((done / total) * 100),
    }


def progress_from_subtasks(subtasks_qs) -> dict:
    total = subtasks_qs.count()
    done = subtasks_qs.filter(status='done').count()
    return activity_progress(done=done, total=total)
