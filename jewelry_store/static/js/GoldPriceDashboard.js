class GoldPriceChart {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.data = [];
    this.chart = null;
    this.exchangeRate = 24350;
    this.currentView = "7days"; // Mặc định xem 7 ngày gần nhất
    this.initializeChart();
  }

  initializeChart() {
    const chartContainer = document.createElement("div");
    chartContainer.className = "gold-price-chart";

    // Tạo tiêu đề và controls
    const header = document.createElement("div");
    header.className = "chart-header";
    header.innerHTML = `
          <h2 class="section-title">Biểu Đồ Giá Vàng</h2>
          <div class="chart-controls">
              <select id="timeRange" class="time-range-select">
                  <option value="7days">7 ngày qua</option>
                  <option value="30days">30 ngày qua</option>
                  <option value="90days">90 ngày qua</option>
              </select>
              <input type="date" id="customDate" class="date-picker" 
                     max="${new Date().toISOString().split("T")[0]}">
          </div>
      `;

    // Tạo bảng giá hiện tại
    const priceTable = document.createElement("div");
    priceTable.className = "current-prices";
    priceTable.innerHTML = `
          <div class="price-card">
              <h3>Giá Vàng SJC Hôm Nay</h3>
              <div class="price-date"></div>
              <div class="price-row">
                  <span>Mua vào:</span>
                  <span class="buy-price">0 ₫</span>
              </div>
              <div class="price-row">
                  <span>Bán ra:</span>
                  <span class="sell-price">0 ₫</span>
              </div>
          </div>
          <div class="price-card">
              <h3>Giá Vàng Thế Giới</h3>
              <div class="price-date"></div>
              <div class="price-row">
                  <span>USD/oz:</span>
                  <span class="world-price">$0</span>
              </div>
              <div class="price-row">
                  <span>VND/chỉ:</span>
                  <span class="world-price-vnd">0 ₫</span>
              </div>
          </div>
      `;

    // Tạo canvas cho biểu đồ
    const canvas = document.createElement("canvas");
    canvas.id = "goldChart";

    chartContainer.appendChild(header);
    chartContainer.appendChild(priceTable);
    chartContainer.appendChild(canvas);
    this.container.appendChild(chartContainer);

    // Thêm event listeners
    const timeRange = document.getElementById("timeRange");
    const customDate = document.getElementById("customDate");

    timeRange.addEventListener("change", (e) => {
      this.currentView = e.target.value;
      this.loadHistoricalData(this.currentView);
    });

    customDate.addEventListener("change", (e) => {
      this.loadSpecificDate(e.target.value);
    });

    // Khởi tạo dữ liệu
    this.loadHistoricalData("7days");
  }

  loadHistoricalData(period) {
    // Giả lập dữ liệu lịch sử
    const days = period === "7days" ? 7 : period === "30days" ? 30 : 90;
    this.data = [];

    for (let i = days - 1; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);

      // Tạo giá ngẫu nhiên nhưng có xu hướng
      const trendFactor = Math.sin(i / 10) * 100000;
      const basePriceBuy = 5900000 + trendFactor;
      const basePriceSell = basePriceBuy + 50000;
      const baseWorldPrice = 2000 + trendFactor / 24350;

      this.data.push({
        date: date.toISOString().split("T")[0],
        buyPrice: basePriceBuy + Math.random() * 50000,
        sellPrice: basePriceSell + Math.random() * 50000,
        worldPrice: baseWorldPrice + Math.random() * 10,
      });
    }

    this.updatePriceTable(this.data[this.data.length - 1]);
    this.drawChart();
  }

  loadSpecificDate(date) {
    // Giả lập dữ liệu cho ngày cụ thể
    const selectedDate = new Date(date);
    const randomFactor = Math.sin(selectedDate.getTime()) * 100000;

    const dayData = {
      date: date,
      buyPrice: 5900000 + randomFactor + Math.random() * 50000,
      sellPrice: 5950000 + randomFactor + Math.random() * 50000,
      worldPrice: 2000 + randomFactor / 24350 + Math.random() * 10,
    };

    this.updatePriceTable(dayData);

    // Hiển thị dữ liệu 7 ngày xung quanh ngày được chọn
    this.data = [];
    for (let i = -3; i <= 3; i++) {
      const currentDate = new Date(selectedDate);
      currentDate.setDate(currentDate.getDate() + i);

      if (currentDate <= new Date()) {
        const trendFactor = Math.sin(i) * 50000;
        this.data.push({
          date: currentDate.toISOString().split("T")[0],
          buyPrice: dayData.buyPrice + trendFactor + Math.random() * 30000,
          sellPrice: dayData.sellPrice + trendFactor + Math.random() * 30000,
          worldPrice:
            dayData.worldPrice + trendFactor / 24350 + Math.random() * 5,
        });
      }
    }

    this.drawChart();
  }

  updatePriceTable(priceData) {
    const buyPriceEl = this.container.querySelector(".buy-price");
    const sellPriceEl = this.container.querySelector(".sell-price");
    const worldPriceEl = this.container.querySelector(".world-price");
    const worldPriceVndEl = this.container.querySelector(".world-price-vnd");
    const priceDates = this.container.querySelectorAll(".price-date");

    const worldPriceVnd = this.convertWorldPriceToVND(priceData.worldPrice);

    buyPriceEl.textContent = this.formatVND(priceData.buyPrice);
    sellPriceEl.textContent = this.formatVND(priceData.sellPrice);
    worldPriceEl.textContent = `$${priceData.worldPrice.toFixed(2)}`;
    worldPriceVndEl.textContent = this.formatVND(worldPriceVnd);

    // Cập nhật ngày
    const formattedDate = new Date(priceData.date).toLocaleDateString("vi-VN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
    priceDates.forEach((el) => (el.textContent = formattedDate));
  }

  convertWorldPriceToVND(usdPrice) {
    return (usdPrice * this.exchangeRate * 3.75) / 31.1034768;
  }

  formatVND(value) {
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(value);
  }

  drawChart() {
    if (this.chart) {
      this.chart.destroy();
    }

    const ctx = document.getElementById("goldChart").getContext("2d");
    this.chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: this.data.map((item) =>
          new Date(item.date).toLocaleDateString("vi-VN")
        ),
        datasets: [
          {
            label: "Giá mua vào",
            data: this.data.map((item) => item.buyPrice),
            borderColor: "#4CAF50",
            backgroundColor: "rgba(76, 175, 80, 0.1)",
            borderWidth: 2,
            fill: false,
          },
          {
            label: "Giá bán ra",
            data: this.data.map((item) => item.sellPrice),
            borderColor: "#F44336",
            backgroundColor: "rgba(244, 67, 54, 0.1)",
            borderWidth: 2,
            fill: false,
          },
          {
            label: "Giá thế giới (VND/chỉ)",
            data: this.data.map((item) =>
              this.convertWorldPriceToVND(item.worldPrice)
            ),
            borderColor: "#2196F3",
            backgroundColor: "rgba(33, 150, 243, 0.1)",
            borderWidth: 2,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                let value = context.raw;
                return new Intl.NumberFormat("vi-VN", {
                  style: "currency",
                  currency: "VND",
                  maximumFractionDigits: 0,
                }).format(value);
              },
            },
          },
        },
        scales: {
          y: {
            ticks: {
              callback: function (value) {
                return new Intl.NumberFormat("vi-VN", {
                  style: "currency",
                  currency: "VND",
                  maximumFractionDigits: 0,
                }).format(value);
              },
            },
          },
        },
      },
    });
  }
}
