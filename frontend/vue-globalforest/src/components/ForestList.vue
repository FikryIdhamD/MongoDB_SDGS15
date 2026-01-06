<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-success"><i class="bi bi-tree-fill"></i> Data Monitoring Hutan (SDG 15)</h2>
      <button @click="openModal('create')" class="btn btn-success shadow-sm">
        <i class="bi bi-plus-lg"></i> Tambah Log Baru
      </button>
    </div>

    <!-- Filter Section -->
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title">Filter Data</h5>
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Negara</label>
            <input v-model="filterCountry" type="text" class="form-control" placeholder="Filter berdasarkan negara">
          </div>
          <div class="col-md-4">
            <label class="form-label">Penyebab (Driver)</label>
            <input v-model="filterDriver" type="text" class="form-control" placeholder="Filter berdasarkan driver">
          </div>
          <div class="col-md-4">
            <label class="form-label">Tahun</label>
            <input v-model.number="filterYear" type="number" class="form-control" placeholder="Filter berdasarkan tahun">
          </div>
        </div>
        <div class="mt-3">
          <button @click="clearFilters" class="btn btn-outline-secondary">Clear Filter</button>
        </div>
      </div>
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
              <tr v-for="log in displayedLogs" :key="log.id">
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
              <tr v-if="isLoading">
                <td colspan="6" class="text-center py-4"><span class="spinner-border spinner-border-sm text-primary me-2"></span>Memuat data...</td>
              </tr>
              <tr v-else-if="logs.length === 0">
                <td colspan="6" class="text-center py-4 text-muted">Belum ada data di database MongoDB lokal Anda.</td>
              </tr>
              <tr v-else-if="filteredLogs.length === 0 && (filterCountry || filterDriver || filterYear)">
                <td colspan="6" class="text-center py-4 text-muted">Tidak ada data yang cocok dengan filter yang diterapkan.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <nav v-if="totalPages > 1" class="mt-3" aria-label="Data pagination">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">Previous</button>
        </li>
        <li v-for="page in visiblePages" :key="page" class="page-item" :class="{ active: page === currentPage }">
          <button class="page-link" @click="goToPage(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">Next</button>
        </li>
      </ul>
    </nav>

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
import { ref, onMounted, computed } from 'vue';

const API_URL = "http://localhost:8000/cases";

const logs = ref([]);
const isLoading = ref(false);
const modals = ref({ create: false, update: false, delete: false });

const createForm = ref({
  country: '',
  driver: '',
  year: new Date().getFullYear(),
  loss: null,
  threshold: 30
});

const updateForm = ref({ country: '', driver: '', year: null, loss: null });

// Filters
const filterCountry = ref('');
const filterDriver = ref('');
const filterYear = ref(null);

// Pagination
const currentPage = ref(1);
const itemsPerPage = 25;

const filteredLogs = computed(() => {
  return logs.value.filter(log => {
    const matchesCountry = !filterCountry.value || log.country.toLowerCase().includes(filterCountry.value.toLowerCase());
    const matchesDriver = !filterDriver.value || log.driver.toLowerCase().includes(filterDriver.value.toLowerCase());
    const matchesYear = !filterYear.value || log.year === filterYear.value;
    return matchesCountry && matchesDriver && matchesYear;
  });
});

const totalPages = computed(() => Math.ceil(filteredLogs.value.length / itemsPerPage));

const displayedLogs = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredLogs.value.slice(start, end);
});

const visiblePages = computed(() => {
  const pages = [];
  const start = Math.max(1, currentPage.value - 2);
  const end = Math.min(totalPages.value, currentPage.value + 2);
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

// 1. Ambil Data (READ)
async function loadData() {
  isLoading.value = true;
  try {
    const response = await fetch(API_URL);
    if (response.ok) {
      const rawData = await response.json();
      console.log("Raw Data from API:", rawData); // Cek console browser (F12) untuk melihat data asli
      logs.value = rawData.flatMap(doc => 
        (doc.drivers || []).flatMap(drv => 
          (drv.losses || []).map(l => ({
            id: `${doc._id}_${drv.driver}_${l.year}`,
            realId: doc._id,
            country: doc.country,
            driver: drv.driver,
            year: l.year,
            loss: l.tc_loss_ha,
            threshold: 30
          }))
        )
      );
      currentPage.value = 1; // Reset to first page after loading data
    }
  } catch (err) {
    console.error("Gagal memuat data MongoDB:", err);
  } finally {
    isLoading.value = false;
  }
}

// 2. Tambah Data (CREATE)
async function createLog() {
  try {
    // Format data sesuai backend: { country, driver, losses: [{year, tc_loss_ha}] }
    const payload = {
      country: createForm.value.country,
      driver: createForm.value.driver,
      losses: [{ year: createForm.value.year, tc_loss_ha: createForm.value.loss }]
    };
    const response = await fetch(`${API_URL}`, { // Hapus trailing slash
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
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
    const payload = {
      country: updateForm.value.country,
      driver: updateForm.value.driver,
      year: updateForm.value.year,
      new_data: { tc_loss_ha: updateForm.value.loss }
    };
    const response = await fetch(`${API_URL}`, { // Endpoint /cases (PUT)
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
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
      // Gunakan Query Params untuk DELETE
      const params = new URLSearchParams({ country: log.country, driver: log.driver, year: log.year });
      const response = await fetch(`${API_URL}?${params.toString()}`, { method: "DELETE" });
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
  updateForm.value = { country: log.country, driver: log.driver, year: log.year, loss: log.loss };
  openModal('update');
}

function resetCreateForm() {
  createForm.value = { country: '', driver: '', year: 2024, loss: null, threshold: 30 };
}

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
}

function clearFilters() {
  filterCountry.value = '';
  filterDriver.value = '';
  filterYear.value = null;
  currentPage.value = 1;
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