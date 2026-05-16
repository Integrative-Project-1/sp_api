from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Activity, Subtask

User = get_user_model()


class SubtaskNoteAndProgressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', email='t@test.com', password='pass12345'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.activity = Activity.objects.create(
            user=self.user,
            title='Tarea',
            activity_type='project',
            course='MAT',
            deadline='2026-06-01',
        )
        self.subtask = Subtask.objects.create(
            activity=self.activity,
            name='Sub 1',
            target_date='2026-05-15',
            estimated_hours=2,
            status='pending',
            note='',
        )
        self.patch_url = f'/api/activities/{self.activity.id}/subtasks/{self.subtask.id}/'
        self.detail_url = f'/api/activities/{self.activity.id}/'

    def test_postpone_with_note(self):
        res = self.client.patch(
            self.patch_url,
            {'status': 'postponed', 'note': 'Esperando cliente'},
            format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.subtask.refresh_from_db()
        self.assertEqual(self.subtask.status, 'postponed')
        self.assertEqual(self.subtask.note, 'Esperando cliente')

    def test_reschedule_preserves_note(self):
        self.subtask.note = 'Nota persistente'
        self.subtask.status = 'postponed'
        self.subtask.save()
        res = self.client.patch(
            self.patch_url,
            {'target_date': '2026-05-20', 'estimated_hours': 3},
            format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.subtask.refresh_from_db()
        self.assertEqual(self.subtask.note, 'Nota persistente')
        self.assertEqual(self.subtask.status, 'postponed')

    def test_status_done_without_note_keeps_note(self):
        self.subtask.note = 'Nota persistente'
        self.subtask.status = 'postponed'
        self.subtask.save()
        res = self.client.patch(self.patch_url, {'status': 'done'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.subtask.refresh_from_db()
        self.assertEqual(self.subtask.status, 'done')
        self.assertEqual(self.subtask.note, 'Nota persistente')

    def test_activity_progress_fields(self):
        Subtask.objects.create(
            activity=self.activity,
            name='Sub 2',
            target_date='2026-05-16',
            estimated_hours=1,
            status='done',
        )
        self.subtask.status = 'done'
        self.subtask.save()
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['subtasks_done'], 2)
        self.assertEqual(res.data['subtasks_total'], 2)
        self.assertEqual(res.data['progress_percent'], 100)

    def test_validation_error_format(self):
        res = self.client.patch(
            self.patch_url,
            {'status': 'invalid'},
            format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', res.data)
        self.assertEqual(res.data['error']['code'], 'validation_error')
        self.assertIn('detail', res.data)
