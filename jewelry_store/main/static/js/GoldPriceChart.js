function GoldPriceChart(container) {
  if (!container) {
    console.error("Container element is required");
    return;
  }

  container.innerHTML = `
    <div class="gold-price-chart">
      <h2 class="section-title">Bảng Giá Vàng</h2>
      <div id="current-prices" class="current-prices">Đang cập nhật...</div>
    </div>
  `;

  const pricesContainer = container.querySelector(".current-prices");

  const goldTypes = [
    { key: "24k", label: "Giá Vàng 24K" },
    { key: "18k", label: "Giá Vàng 18K" },
    { key: "14k", label: "Giá Vàng 14K" },
    { key: "9k", label: "Giá Vàng 9K" },
  ];

  function formatVND(value) {
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(value);
  }

  function updatePrices(priceData) {
    if (!priceData || priceData.length === 0) {
      console.warn("Không có dữ liệu giá vàng để hiển thị.");
      pricesContainer.innerHTML = `<p>Không có dữ liệu giá vàng.</p>`;
      return;
    }

    const pricesHTML = goldTypes
      .map(({ key, label }) => {
        const priceInfo = priceData.find((p) =>
          p.loai_vang.toLowerCase().includes(key)
        );

        const date = priceInfo?.ngay
          ? new Date(priceInfo.ngay).toLocaleDateString("vi-VN", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })
          : "Không có ngày cập nhật";

        return `
          <div class="price-card">
            <h3>${label}</h3>
            <div class="price-date">${date}</div>
            <div class="price-row">
              <span>Mua vào:</span>
              <span class="text-green-600">
                ${priceInfo ? formatVND(priceInfo.gia_mua) : "Đang cập nhật..."}
              </span>
            </div>
            <div class="price-row">
              <span>Bán ra:</span>
              <span class="text-red-600">
                ${priceInfo ? formatVND(priceInfo.gia_ban) : "Đang cập nhật..."}
              </span>
            </div>
          </div>
        `;
      })
      .join("");

    pricesContainer.innerHTML = pricesHTML;
  }

  function fetchGoldPrices() {
    fetch("/api/gold-prices/")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Dữ liệu API trả về:", data);
        updatePrices(data);
      })
      .catch((error) => {
        console.error("Lỗi khi gọi API:", error);
        pricesContainer.innerHTML = `<p class="error-message">Không thể tải dữ liệu. Hãy thử lại sau!</p>`;
      });
  }

  fetchGoldPrices();

  setInterval(fetchGoldPrices, 30000);
}

export default GoldPriceChart;
