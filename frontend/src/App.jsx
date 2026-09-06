import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import Layout from "./components/layout/Layout";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Notifications from "./pages/Notifications";
import Settings from "./pages/Settings";

// Agent pages
import Climate from "./pages/Climate";
import CropPlanning from "./pages/CropPlanning";
import CropHealth from "./pages/CropHealth";
import Market from "./pages/Market";
import GovernmentSchemes from "./pages/GovernmentSchemes";
import Knowledge from "./pages/Knowledge";


function App() {
  return (
    <BrowserRouter>

      <Routes>

        {/* =====================================================
            AUTHENTICATION
        ===================================================== */}

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/signup"
          element={<Signup />}
        />


        {/* =====================================================
            DASHBOARD
        ===================================================== */}

        <Route
          path="/dashboard"
          element={
            <Layout>
              <Dashboard />
            </Layout>
          }
        />


        {/* =====================================================
            SETTINGS
        ===================================================== */}

        <Route
          path="/settings"
          element={
            <Layout>
              <Settings />
            </Layout>
          }
        />


        {/* =====================================================
            NOTIFICATIONS
        ===================================================== */}

        <Route
          path="/notifications"
          element={
            <Layout>
              <Notifications />
            </Layout>
          }
        />


        {/* =====================================================
            CLIMATE INTELLIGENCE
        ===================================================== */}

        <Route
          path="/climate"
          element={
            <Layout>
              <Climate />
            </Layout>
          }
        />


        {/* =====================================================
            CROP PLANNING
        ===================================================== */}

        <Route
          path="/crop-planning"
          element={
            <Layout>
              <CropPlanning />
            </Layout>
          }
        />


        {/* =====================================================
            CROP HEALTH
        ===================================================== */}

        <Route
          path="/crop-health"
          element={
            <Layout>
              <CropHealth />
            </Layout>
          }
        />


        {/* =====================================================
            MARKET INTELLIGENCE
        ===================================================== */}

        <Route
          path="/market"
          element={
            <Layout>
              <Market />
            </Layout>
          }
        />


        {/* =====================================================
            GOVERNMENT SCHEMES
        ===================================================== */}

        <Route
          path="/government-schemes"
          element={
            <Layout>
              <GovernmentSchemes />
            </Layout>
          }
        />


        {/* =====================================================
            AI KNOWLEDGE
        ===================================================== */}

        <Route
          path="/knowledge"
          element={
            <Layout>
              <Knowledge />
            </Layout>
          }
        />


        {/* =====================================================
            DEFAULT ROUTE
        ===================================================== */}

        <Route
          path="/"
          element={
            <Navigate
              to="/dashboard"
              replace
            />
          }
        />


        {/* =====================================================
            UNKNOWN ROUTES
        ===================================================== */}

        <Route
          path="*"
          element={
            <Navigate
              to="/dashboard"
              replace
            />
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;