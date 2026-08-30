import {
  LayoutDashboard,
  CloudSun,
  Sprout,
  Leaf,
  TrendingUp,
  Landmark,
  MessageCircle,
  BrainCircuit,
  Bell,
  Settings,
  User,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

const menuItems = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    label: "Climate Intelligence",
    icon: CloudSun,
    path: "/climate",
  },
  {
    label: "Crop Planning",
    icon: Sprout,
    path: "/crop-planning",
  },
  {
    label: "Crop Health",
    icon: Leaf,
    path: "/crop-health",
  },
  {
    label: "Market Intelligence",
    icon: TrendingUp,
    path: "/market",
  },
  {
    label: "Government Schemes",
    icon: Landmark,
    path: "/government-schemes",
  },
  {
    label: "AI Knowledge",
    icon: MessageCircle,
    path: "/knowledge",
  },
  {
    label: "AI Recommendations",
    icon: BrainCircuit,
    path: "/recommendations",
  },
];

const bottomItems = [
  {
    label: "Notifications",
    icon: Bell,
    path: "/notifications",
  },
  {
    label: "Profile",
    icon: User,
    path: "/profile",
  },
  {
    label: "Settings",
    icon: Settings,
    path: "/settings",
  },
];

function Sidebar({
  collapsed,
  setCollapsed,
  currentPath,
  navigate,
}) {
  const renderItem = (item) => {
    const Icon = item.icon;

    const active =
      currentPath === item.path ||
      currentPath.startsWith(`${item.path}/`);

    return (
      <button
        key={item.path}
        type="button"
        onClick={() => navigate(item.path)}
        title={collapsed ? item.label : ""}
        className={`sidebar-item ${
          active ? "active" : ""
        }`}
      >
        <Icon
          size={20}
          strokeWidth={2}
        />

        {!collapsed && (
          <span>{item.label}</span>
        )}
      </button>
    );
  };

  return (
    <aside
      className={`sidebar ${
        collapsed
          ? "sidebar-collapsed"
          : ""
      }`}
    >

      {/* =====================================================
          BRAND
      ===================================================== */}

      <div className="sidebar-brand">

        <div className="brand-icon">
          <Sprout size={24} />
        </div>

        {!collapsed && (
          <div className="brand-text">
            <strong>AgriSphere</strong>
            <span>AI</span>
          </div>
        )}

      </div>

      {/* =====================================================
          MAIN NAVIGATION
      ===================================================== */}

      <div className="sidebar-section">

        {!collapsed && (
          <p className="sidebar-label">
            INTELLIGENCE
          </p>
        )}

        <nav>
          {menuItems.map(renderItem)}
        </nav>

      </div>

      {/* =====================================================
          ACCOUNT NAVIGATION
      ===================================================== */}

      <div className="sidebar-bottom">

        {!collapsed && (
          <p className="sidebar-label">
            ACCOUNT
          </p>
        )}

        <nav>
          {bottomItems.map(renderItem)}
        </nav>

      </div>

      {/* =====================================================
          COLLAPSE BUTTON
      ===================================================== */}

      <button
        type="button"
        className="sidebar-collapse"
        onClick={() =>
          setCollapsed(!collapsed)
        }
        title={
          collapsed
            ? "Expand sidebar"
            : "Collapse sidebar"
        }
      >

        {collapsed ? (
          <ChevronRight size={18} />
        ) : (
          <ChevronLeft size={18} />
        )}

        {!collapsed && (
          <span>Collapse</span>
        )}

      </button>

    </aside>
  );
}

export default Sidebar;