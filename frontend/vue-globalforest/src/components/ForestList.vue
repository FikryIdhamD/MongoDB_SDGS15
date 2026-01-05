<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-success"><i class="bi bi-tree-fill"></i> Data Monitoring Hutan (SDG 15)</h2>
      <button @click="openModal('create')" class="btn btn-success shadow-sm">
        <i class="bi bi-plus-lg"></i> Tambah Log Baru
      </button>
    </div>

    <div class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-dark">
              <tr>
                <th>Country</th>
                <th>Driver</th>
                <th>Year</th>
                <th>Loss (Ha)</th>
                <th>Threshold</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in logs" :key="log.id">
                <td class="fw-bold">{{ log.country }}</td>
                <td><span class="badge bg-info text-dark">{{ log.driver }}</span></td>
                <td>{{ log.year }}</td>
                <td>{{ log.loss.toLocaleString() }} ha</td>
                <td>{{ log.threshold }}%</td>
                <td class="text-center">
                  <button @click="openUpdateModal(log)" class="btn btn-outline-primary btn-sm me-2">
                    <i class="bi bi-pencil-square"></i> Edit
                  </button>
                  <button @click="openDeleteModal(log)" class="btn btn-outline-danger btn-sm">
                    <i class="bi bi-trash"></i> Hapus
                  </button>
                </td>
              </tr>
              <tr v-if="logs.length === 0">
                <td colspan="6" class="text-center py-4 text-muted">Belum ada data di database MongoDB lokal Anda.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="modal-backdrop" v-if="modals.create">
      <div class="custom-modal shadow-lg">
        <div class="modal-header">
          <h5 class="m-0">Tambah Log Kerusakan Hutan</h5>
          <button type="button" class="btn-close" @click="closeModal('create')"></button>
        </div>
        <form @submit.prevent="createLog">
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Negara</label>
              <input v-model="createForm.country" type="text" class="form-control" placeholder="Contoh: Indonesia" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Penyebab (Driver)</label>
              <input v-model="createForm.driver" type="text" class="form-control" placeholder="Contoh: Fire, Logging" required>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Tahun</label>
                <input v-model.number="createForm.year" type="number" class="form-control" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Threshold (%)</label>
                <input v-model.number="createForm.threshold" type="number" class="form-control">
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Luas Kehilangan (Hektar)</label>
              <input v-model.number="createForm.loss" type="number" step="0.01" class="form-control" required>
            </div>
          </div>
          <div class="modal-footer bg-light">
            <button type="button" class="btn btn-secondary" @click="closeModal('create')">Batal</button>
            <button type="submit" class="btn btn-success">Simpan Data</button>
          </div>
        </form>
      </div>
    </div>

    <div class="modal-backdrop" v-if="modals.update">
      <div class="custom-modal shadow-lg border-primary">
        <div class="modal-header bg-primary text-white">
          <h5 class="m-0">Update Data Log</h5>
          <button type="button" class="btn-close btn-close-white" @click="closeModal('update')"></button>
        </div>
        <form @submit.prevent="updateLog">
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Negara</label>
              <input v-model="updateForm.country" type="text" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Luas Kehilangan (Hektar)</label>
              <input v-model.number="updateForm.loss" type="number" step="0.01" class="form-control" required>
            </div>
          </div>
          <div class="modal-footer bg-light">
            <button type="button" class="btn btn-secondary" @click="closeModal('update')">Batal</button>
            <button type="submit" class="btn btn-primary">Update Perubahan</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Konfigurasi API - Gunakan prefix /api/forest sesuai main.py
const API_URL = "http://localhost:8000/api/forest";

const logs = ref([]);
const modals = ref({ create: false, update: false, delete: false });

const createForm = ref({
  country: '',
  driver: '',
  year: new Date().getFullYear(),
  loss: null,
  threshold: 30
});

const updateForm = ref({ id: '', country: '', loss: null });

// 1. Ambil Data (READ)
async function loadData() {
  try {
    const response = await fetch(`${API_URL}/`);
    if (response.ok) {
      logs.value = await response.json();
    }
  } catch (err) {
    console.error("Gagal memuat data MongoDB:", err);
  }
}

// 2. Tambah Data (CREATE)
async function createLog() {
  try {
    const response = await fetch(`${API_URL}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(createForm.value)
    });
    
    if (response.ok) {
      closeModal('create');
      loadData(); // Refresh tabel
      resetCreateForm();
    }
  } catch (err) {
    alert("Gagal menambah data!");
  }
}

// 3. Update Data (UPDATE)
async function updateLog() {
  try {
    const response = await fetch(`${API_URL}/log/${updateForm.value.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updateForm.value)
    });
    
    if (response.ok) {
      closeModal('update');
      loadData();
    }
  } catch (err) {
    alert("Gagal update data!");
  }
}

// 4. Hapus Data (DELETE)
async function openDeleteModal(log) {
  if (confirm(`Apakah Anda yakin ingin menghapus data log untuk negara ${log.country}?`)) {
    try {
      const response = await fetch(`${API_URL}/log/${log.id}`, { method: "DELETE" });
      if (response.ok) loadData();
    } catch (err) {
      alert("Gagal menghapus data!");
    }
  }
}

// UI Helpers
function openModal(id) { modals.value[id] = true; }
function closeModal(id) { modals.value[id] = false; }

function openUpdateModal(log) {
  updateForm.value = { id: log.id, country: log.country, loss: log.loss };
  openModal('update');
}

function resetCreateForm() {
  createForm.value = { country: '', driver: '', year: 2024, loss: null, threshold: 30 };
}

onMounted(loadData);
</script>

<style scoped>
/* Modal Style agar tampilan lebih profesional untuk UAS */
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.custom-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dee2e6;
}

.modal-body { padding: 20px; }
.modal-footer { padding: 15px 20px; display: flex; justify-content: flex-end; gap: 10px; }

/* Responsive Table */
.table th { font-weight: 600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.5px; }
</style>