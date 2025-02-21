import React from "react";
import { createRoot } from "react-dom/client";
import ProductGrid from "./components/ProductGrid";

const container = document.getElementById("product-grid-root");
const root = createRoot(container);
root.render(<ProductGrid initialData={window.initialData} />);
