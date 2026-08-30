import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

function Layout({ children }) {
  const [collapsed, setCollapsed] =
    useState(false);

  const location = useLocation();
  const navigate = useNavigate();

  return (
    <div className="app-layout">

      <Sidebar
        collapsed={collapsed}
        setCollapsed={setCollapsed}
        currentPath={location.pathname}
        navigate={navigate}
      />

      <div
        className={`app-main ${
          collapsed ? "main-expanded" : ""
        }`}
      >

        <Navbar />

        <main className="page-content">
          {children}
        </main>

      </div>

    </div>
  );
}

export default Layout;