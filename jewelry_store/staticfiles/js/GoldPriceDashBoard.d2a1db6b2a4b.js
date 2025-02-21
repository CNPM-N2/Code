class GoldPriceChart {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.error(`Container with id ${containerId} not found`);
      return;
    }
    this.initializeChart();
  }

  initializeChart() {
    const chartContainer = document.createElement("div");
    chartContainer.className = "gold-price-chart";

    const header = document.createElement("div");
    header.className = "chart-header";
    header.innerHTML = `
          <h2 class="section-title">Bảng Giá Vàng</h2>
      `;

    const priceTable = document.createElement("div");
    priceTable.className = "current-prices";
    priceTable.innerHTML = `
          <div class="price-card">
              <h3>Giá Vàng 24K</h3>
              <div class="price-date"></div>
              <div class="price-row">
                  <span>Mua vào:</span>
                  <span class="buy-price-24k">0 ₫</span>
              </div>
              <div class="price-row">
                  <span>Bán ra:</span>
                  <span class="sell-price-24k">0 ₫</span>
              </div>
          </div>
          <div class="price-card">
              <h3>Giá Vàng 18K</h3>
              <div class="price-date"></div>
              <div class="price-row">
                  <span>Mua vào:</span>
                  <span class="buy-price-18k">0 ₫</span>
              </div>
              <div class="price-row">
                  <span>Bán ra:</span>
                  <span class="sell-price-18k">0 ₫</span>
              </div>
          </div>
          <div class="price-card">
              <h3>Giá Vàng 14K</h3>
              <div class="price-date"></div>
              <div class="price-row">
                  <span>Mua vào:</span>
                  <span class="buy-price-14k">0 ₫</span>
              </div>
              <div class="price-row">
                  <span>Bán ra:</span>
                  <span class="sell-price-14k">0 ₫</span>
              </div>
          </div>
          <div class="price-card">
              <h3>Giá Vàng 9K</h3>
              <div class="price-date"></div>
              <div class="price-row">
                  <span>Mua vào:</span>
                  <span class="buy-price-9k">0 ₫</span>
              </div>
              <div class="price-row">
                  <span>Bán ra:</span>
                  <span class="sell-price-9k">0 ₫</span>
              </div>
          </div>
      `;

    chartContainer.appendChild(header);
    chartContainer.appendChild(priceTable);
    this.container.appendChild(chartContainer);

    this.loadCurrentPrices();
  }

  async loadCurrentPrices() {
    try {
      const response = await fetch("/api/gold-prices/current/");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      this.updatePriceTable(data);
    } catch (error) {
      console.error("Error fetching gold prices:", error);
      this.showError("Không thể tải dữ liệu giá vàng");
    }
  }

  updatePriceTable(priceData) {
    const priceDates = this.container.querySelectorAll(".price-date");
    const formattedDate = new Date(priceData.date).toLocaleDateString("vi-VN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });

    ["24k", "18k", "14k", "9k"].forEach((type) => {
      if (priceData.prices[type]) {
        const buyPrice = this.container.querySelector(`.buy-price-${type}`);
        const sellPrice = this.container.querySelector(`.sell-price-${type}`);

        if (buyPrice && sellPrice) {
          buyPrice.textContent = this.formatVND(priceData.prices[type].buy);
          sellPrice.textContent = this.formatVND(priceData.prices[type].sell);
        }
      }
    });

    priceDates.forEach((el) => (el.textContent = formattedDate));
  }

  formatVND(value) {
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(value);
  }

  showError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.textContent = message;
    this.container.appendChild(errorDiv);
  }
}

// Export the class for use in other files
window.GoldPriceChart = GoldPriceChart;
