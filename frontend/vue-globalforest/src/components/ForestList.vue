<template>
  
  <div class="container mt-4">
    <!-- News Section -->
    <div class="mt-4">
      <h3 class="text-success mb-3"><i class="bi bi-newspaper"></i> Berita Terkini SDG 15 - Hutan</h3>
      <div class="row">
        <div v-for="news in newsItems" :key="news.id" class="col-md-4 mb-3">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ news.title }}</h5>
              <p class="card-text">{{ news.summary }}</p>
              <small class="text-muted">{{ news.date }}</small>
            </div>
            <div class="card-footer">
              <a :href="news.link" target="_blank" class="btn btn-outline-success btn-sm">Baca Selengkapnya</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Conservation Tips Section -->
    <div class="mt-4">
      <h3 class="text-success mb-3"><i class="bi bi-lightbulb"></i> Tips Konservasi Hutan</h3>
      <div class="row">
        <div v-for="tip in conservationTips" :key="tip.id" class="col-md-4 mb-3">
          <div class="card h-100 shadow-sm border-success">
            <div class="card-body">
              <h5 class="card-title text-success">{{ tip.title }}</h5>
              <p class="card-text">{{ tip.description }}</p>
            </div>
            <div class="card-footer bg-success bg-opacity-10">
              <small class="text-muted">{{ tip.category }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Statistics Section -->
    <div class="mt-4">
      <h3 class="text-success mb-3"><i class="bi bi-bar-chart"></i> Statistik SDG 15 - Kerusakan Hutan</h3>
      <div class="row">
        <div class="col-md-6 mb-3">
          <div class="card shadow-sm">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Kerusakan Hutan per Negara (Top 5)</h5>
            </div>
            <div class="card-body">
              <div v-for="stat in countryStats" :key="stat.country" class="mb-2">
                <div class="d-flex justify-content-between">
                  <span>{{ stat.country }}</span>
                  <span>{{ stat.totalLoss.toLocaleString() }} ha</span>
                </div>
                <div class="progress" style="height: 20px;">
                  <div class="progress-bar bg-danger" :style="{ width: stat.percentage + '%' }" role="progressbar" :aria-valuenow="stat.percentage" aria-valuemin="0" aria-valuemax="100">
                    {{ stat.percentage }}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 mb-3">
          <div class="card shadow-sm">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Kerusakan Hutan per Penyebab</h5>
            </div>
            <div class="card-body">
              <div v-for="stat in driverStats" :key="stat.driver" class="mb-2">
                <div class="d-flex justify-content-between">
                  <span>{{ stat.driver }}</span>
                  <span>{{ stat.totalLoss.toLocaleString() }} ha</span>
                </div>
                <div class="progress" style="height: 20px;">
                  <div class="progress-bar bg-warning" :style="{ width: stat.percentage + '%' }" role="progressbar" :aria-valuenow="stat.percentage" aria-valuemin="0" aria-valuemax="100">
                    {{ stat.percentage }}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Charts Section -->
    <div class="mt-4">
      <h3 class="text-success mb-3"><i class="bi bi-graph-up"></i> Grafik Analisis SDG 15</h3>
      <div class="row">
        <div class="col-md-6 mb-3">
          <div class="card shadow-sm">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Grafik Batang - Kerusakan per Negara</h5>
            </div>
            <div class="card-body">
              <svg width="100%" height="200" viewBox="0 0 400 200">
                <g v-for="(stat, index) in countryStats.slice(0, 5)" :key="stat.country">
                  <rect :x="index * 70 + 20" y="180" :width="40" :height="-(stat.totalLoss / maxLoss * 150)" fill="#dc3545" stroke="#000" stroke-width="1"/>
                  <text :x="index * 70 + 40" y="195" text-anchor="middle" font-size="10">{{ stat.country }}</text>
                  <text :x="index * 70 + 40" :y="175 - (stat.totalLoss / maxLoss * 150)" text-anchor="middle" font-size="8" fill="#fff">{{ stat.totalLoss.toFixed(0) }}</text>
                </g>
              </svg>
            </div>
          </div>
        </div>
        <div class="col-md-6 mb-3">
          <div class="card shadow-sm">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Grafik Garis - Tren Kerusakan per Tahun</h5>
            </div>
            <div class="card-body">
              <svg width="100%" height="200" viewBox="0 0 400 200">
                <polyline :points="yearlyTrendPoints" fill="none" stroke="#ffc107" stroke-width="3"/>
                <g v-for="(point, index) in yearlyTrend" :key="point.year">
                  <circle :cx="index * 60 + 40" :cy="180 - (point.loss / maxYearlyLoss * 150)" r="4" fill="#ffc107"/>
                  <text :x="index * 60 + 40" y="195" text-anchor="middle" font-size="10">{{ point.year }}</text>
                </g>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Custom Charts Section -->
    <div class="mt-4">
      <h3 class="text-success mb-3"><i class="bi bi-bar-chart-line"></i> Grafik Kustom SDG 15</h3>
      <div class="card shadow-sm mb-3">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">Filter berdasarkan Negara</label>
              <select v-model="chartFilterCountry" class="form-select">
                <option value="">Semua Negara</option>
                <option v-for="country in uniqueCountries" :key="country" :value="country">{{ country }}</option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label">Filter berdasarkan Driver</label>
              <select v-model="chartFilterDriver" class="form-select">
                <option value="">Semua Driver</option>
                <option v-for="driver in uniqueDrivers" :key="driver" :value="driver">{{ driver }}</option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label">Tipe Grafik</label>
              <select v-model="chartType" class="form-select">
                <option value="line">Grafik Garis (Tren per Tahun)</option>
                <option value="bar">Grafik Batang (Loss per Kategori)</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <div class="card shadow-sm">
        <div class="card-header bg-success text-white">
          <h5 class="mb-0">{{ chartTitle }}</h5>
        </div>
        <div class="card-body">
          <div v-if="chartType === 'line'">
            <svg width="100%" height="250" viewBox="0 0 500 250">
              <polyline :points="customLinePoints" fill="none" stroke="#28a745" stroke-width="3"/>
              <g v-for="(point, index) in customLineData" :key="point.year">
                <circle :cx="index * 70 + 50" :cy="220 - (point.loss / customMaxLoss * 180)" r="5" fill="#28a745"/>
                <text :x="index * 70 + 50" y="240" text-anchor="middle" font-size="10">{{ point.year }}</text>
                <text :x="index * 70 + 50" :y="210 - (point.loss / customMaxLoss * 180)" text-anchor="middle" font-size="9" fill="#000">{{ point.loss.toFixed(0) }}</text>
              </g>
            </svg>
          </div>
          <div v-else>
            <svg width="100%" height="250" viewBox="0 0 500 250">
              <g v-for="(stat, index) in customBarData" :key="stat.label">
                <rect :x="index * 80 + 30" y="220" :width="50" :height="-(stat.value / customMaxBar * 180)" fill="#17a2b8" stroke="#000" stroke-width="1"/>
                <text :x="index * 80 + 55" y="235" text-anchor="middle" font-size="10" transform="rotate(-45, index * 80 + 55, 235)">{{ stat.label }}</text>
                <text :x="index * 80 + 55" :y="215 - (stat.value / customMaxBar * 180)" text-anchor="middle" font-size="9" fill="#fff">{{ stat.value.toFixed(0) }}</text>
              </g>
            </svg>
          </div>
        </div>
      </div>
    </div>
    <br>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-success"><i class="bi bi-tree-fill"></i> Data Monitoring Hutan</h2>
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
                <th @click="sortByColumn('country')" style="cursor: pointer;">Country <i v-if="sortBy === 'country'" :class="sortOrder === 'asc' ? 'bi bi-chevron-up' : 'bi bi-chevron-down'"></i></th>
                <th>Driver</th>
                <th>Year</th>
                <th>Loss (Ha)</th>
                <th>Threshold</th>
                <!-- <th class="text-center">Actions</th> -->
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in displayedLogs" :key="log.id">
                <td class="fw-bold">{{ log.country }}</td>
                <td><span class="badge bg-info text-dark">{{ log.driver }}</span></td>
                <td>{{ log.year }}</td>
                <td>{{ log.loss.toLocaleString() }} ha</td>
                <td>{{ log.threshold }}%</td>
                <!-- <td class="text-center">
                  <button @click="openUpdateModal(log)" class="btn btn-outline-primary btn-sm me-2">
                    <i class="bi bi-pencil-square"></i> Edit
                  </button>
                  <button @click="openDeleteModal(log)" class="btn btn-outline-danger btn-sm">
                    <i class="bi bi-trash"></i> Hapus
                  </button>
                </td> -->
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

// News Items
const newsItems = ref([
  {
    id: 1,
    title: "Krisis Deforestasi Global Meningkat",
    summary: "Laporan terbaru menunjukkan deforestasi di Amazon mencapai rekor tertinggi tahun ini.",
    date: "6 Januari 2026",
    link: "#"
  },
  {
    id: 2,
    title: "Inisiatif Reboisasi di Indonesia",
    summary: "Pemerintah Indonesia meluncurkan program penanaman 1 juta pohon untuk mengatasi kerusakan hutan.",
    date: "5 Januari 2026",
    link: "#"
  },
  {
    id: 3,
    title: "Dampak Perubahan Iklim pada Hutan",
    summary: "Studi ilmiah mengungkapkan bagaimana perubahan iklim mempercepat kerusakan ekosistem hutan.",
    date: "4 Januari 2026",
    link: "#"
  }
]);

// Conservation Tips
const conservationTips = ref([
  {
    id: 1,
    title: "Tanam Pohon Setiap Hari",
    description: "Mulai kebiasaan menanam pohon di halaman rumah atau area publik untuk berkontribusi pada reboisasi.",
    category: "Aksi Individu"
  },
  {
    id: 2,
    title: "Kurangi Penggunaan Kertas",
    description: "Gunakan kertas daur ulang dan minimalkan pencetakan untuk mengurangi tebang pohon.",
    category: "Penghematan Sumber Daya"
  },
  {
    id: 3,
    title: "Dukung Produk Ramah Lingkungan",
    description: "Pilih produk dari bahan daur ulang dan hindari barang yang berkontribusi pada deforestasi.",
    category: "Konsumsi Bijak"
  }
]);

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

// Sorting
const sortBy = ref('country');
const sortOrder = ref('asc');

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

const sortedLogs = computed(() => {
  return [...filteredLogs.value].sort((a, b) => {
    let aVal = a[sortBy.value];
    let bVal = b[sortBy.value];
    if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase();
      bVal = bVal.toLowerCase();
    }
    if (sortOrder.value === 'asc') {
      return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
    } else {
      return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
    }
  });
});

const totalPages = computed(() => Math.ceil(sortedLogs.value.length / itemsPerPage));

const displayedLogs = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return sortedLogs.value.slice(start, end);
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

const countryStats = computed(() => {
  const stats = {};
  logs.value.forEach(log => {
    if (!stats[log.country]) stats[log.country] = 0;
    stats[log.country] += log.loss;
  });
  const total = Object.values(stats).reduce((sum, val) => sum + val, 0);
  return Object.entries(stats)
    .map(([country, loss]) => ({ country, totalLoss: loss, percentage: Math.round((loss / total) * 100) }))
    .sort((a, b) => b.totalLoss - a.totalLoss)
    .slice(0, 5);
});

const driverStats = computed(() => {
  const stats = {};
  logs.value.forEach(log => {
    if (!stats[log.driver]) stats[log.driver] = 0;
    stats[log.driver] += log.loss;
  });
  const total = Object.values(stats).reduce((sum, val) => sum + val, 0);
  return Object.entries(stats)
    .map(([driver, loss]) => ({ driver, totalLoss: loss, percentage: Math.round((loss / total) * 100) }))
    .sort((a, b) => b.totalLoss - a.totalLoss);
});

const maxLoss = computed(() => {
  return Math.max(...countryStats.value.map(stat => stat.totalLoss), 1);
});

const yearlyTrend = computed(() => {
  const stats = {};
  logs.value.forEach(log => {
    if (!stats[log.year]) stats[log.year] = 0;
    stats[log.year] += log.loss;
  });
  return Object.entries(stats)
    .map(([year, loss]) => ({ year: parseInt(year), loss }))
    .sort((a, b) => a.year - b.year)
    .slice(-6); // Last 6 years
});

const maxYearlyLoss = computed(() => {
  return Math.max(...yearlyTrend.value.map(point => point.loss), 1);
});

const yearlyTrendPoints = computed(() => {
  return yearlyTrend.value.map((point, index) => 
    `${index * 60 + 40},${180 - (point.loss / maxYearlyLoss.value * 150)}`
  ).join(' ');
});

// Custom Chart Filters
const chartFilterCountry = ref('');
const chartFilterDriver = ref('');
const chartType = ref('line');

const uniqueCountries = computed(() => {
  const countries = new Set(logs.value.map(log => log.country));
  return Array.from(countries).sort();
});

const uniqueDrivers = computed(() => {
  const drivers = new Set(logs.value.map(log => log.driver));
  return Array.from(drivers).sort();
});

const chartTitle = computed(() => {
  let title = chartType.value === 'line' ? 'Grafik Garis' : 'Grafik Batang';
  if (chartFilterCountry.value) title += ` - ${chartFilterCountry.value}`;
  if (chartFilterDriver.value) title += ` (${chartFilterDriver.value})`;
  return title;
});

const filteredChartData = computed(() => {
  return logs.value.filter(log => {
    return (!chartFilterCountry.value || log.country === chartFilterCountry.value) &&
           (!chartFilterDriver.value || log.driver === chartFilterDriver.value);
  });
});

const customLineData = computed(() => {
  const stats = {};
  filteredChartData.value.forEach(log => {
    if (!stats[log.year]) stats[log.year] = 0;
    stats[log.year] += log.loss;
  });
  return Object.entries(stats)
    .map(([year, loss]) => ({ year: parseInt(year), loss }))
    .sort((a, b) => a.year - b.year);
});

const customMaxLoss = computed(() => {
  return Math.max(...customLineData.value.map(point => point.loss), 1);
});

const customLinePoints = computed(() => {
  return customLineData.value.map((point, index) => 
    `${index * 70 + 50},${220 - (point.loss / customMaxLoss.value * 180)}`
  ).join(' ');
});

const customBarData = computed(() => {
  if (chartFilterCountry.value && !chartFilterDriver.value) {
    // Bar chart by driver for selected country
    const stats = {};
    filteredChartData.value.forEach(log => {
      if (!stats[log.driver]) stats[log.driver] = 0;
      stats[log.driver] += log.loss;
    });
    return Object.entries(stats).map(([driver, loss]) => ({ label: driver, value: loss }));
  } else if (chartFilterDriver.value && !chartFilterCountry.value) {
    // Bar chart by country for selected driver
    const stats = {};
    filteredChartData.value.forEach(log => {
      if (!stats[log.country]) stats[log.country] = 0;
      stats[log.country] += log.loss;
    });
    return Object.entries(stats).map(([country, loss]) => ({ label: country, value: loss }));
  } else {
    // Default: bar chart by country
    const stats = {};
    filteredChartData.value.forEach(log => {
      if (!stats[log.country]) stats[log.country] = 0;
      stats[log.country] += log.loss;
    });
    return Object.entries(stats).map(([country, loss]) => ({ label: country, value: loss })).slice(0, 5);
  }
});

const customMaxBar = computed(() => {
  return Math.max(...customBarData.value.map(stat => stat.value), 1);
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

function sortByColumn(column) {
  if (sortBy.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortBy.value = column;
    sortOrder.value = 'asc';
  }
  currentPage.value = 1; // Reset to first page when sorting
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