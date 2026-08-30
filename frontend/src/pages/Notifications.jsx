import { useEffect, useState } from "react";

import {
  Bell,
  CloudSun,
  Leaf,
  TrendingUp,
  Landmark,
  BrainCircuit,
  Check,
  CheckCheck,
  Trash2,
  Filter,
  AlertTriangle,
  Info,
  CircleCheck,
  Clock3,
} from "lucide-react";


/* =========================================================
   DEFAULT NOTIFICATIONS
========================================================= */

const DEFAULT_NOTIFICATIONS = [

  {
    id: 1,
    type: "climate",
    title: "Climate monitoring active",
    message:
      "AgriSphere is ready to monitor weather conditions and farming risks for your location.",
    time: "Just now",
    read: false,
    priority: "normal",
  },

  {
    id: 2,
    type: "crop",
    title: "Keep monitoring crop health",
    message:
      "Upload a fresh crop image regularly to track changes in crop health and detect visible symptoms.",
    time: "Today",
    read: false,
    priority: "normal",
  },

  {
    id: 3,
    type: "market",
    title: "Market intelligence available",
    message:
      "Check the Market Intelligence section to review current crop price trends.",
    time: "Today",
    read: true,
    priority: "normal",
  },

  {
    id: 4,
    type: "government",
    title: "Check government schemes",
    message:
      "New agricultural schemes and application opportunities may become available. Review your eligible schemes regularly.",
    time: "Yesterday",
    read: true,
    priority: "important",
  },

  {
    id: 5,
    type: "recommendation",
    title: "AI recommendations ready",
    message:
      "Use AI Recommendations to receive farming actions based on your crop and location.",
    time: "Yesterday",
    read: true,
    priority: "normal",
  },

];


/* =========================================================
   ICONS
========================================================= */

const notificationIcons = {

  climate: CloudSun,

  crop: Leaf,

  market: TrendingUp,

  government: Landmark,

  recommendation: BrainCircuit,

};


/* =========================================================
   MAIN COMPONENT
========================================================= */

function Notifications() {

  const [notifications, setNotifications] =
    useState([]);

  const [filter, setFilter] =
    useState("all");


  /* =====================================================
     LOAD NOTIFICATIONS
  ===================================================== */

  useEffect(() => {

    try {

      const stored =
        localStorage.getItem(
          "agrisphere_notifications"
        );


      if (stored) {

        setNotifications(
          JSON.parse(stored)
        );

      } else {

        setNotifications(
          DEFAULT_NOTIFICATIONS
        );

        localStorage.setItem(
          "agrisphere_notifications",
          JSON.stringify(
            DEFAULT_NOTIFICATIONS
          )
        );

      }

    } catch (error) {

      console.error(
        "Unable to load notifications:",
        error
      );

      setNotifications(
        DEFAULT_NOTIFICATIONS
      );

    }

  }, []);


  /* =====================================================
     SAVE NOTIFICATIONS
  ===================================================== */

  useEffect(() => {

    if (
      notifications.length >= 0
    ) {

      localStorage.setItem(
        "agrisphere_notifications",
        JSON.stringify(
          notifications
        )
      );

    }

  }, [notifications]);


  /* =====================================================
     MARK ONE READ
  ===================================================== */

  const markAsRead = (id) => {

    setNotifications(
      (previous) =>
        previous.map(
          (notification) =>
            notification.id === id
              ? {
                  ...notification,
                  read: true,
                }
              : notification
        )
    );

  };


  /* =====================================================
     MARK ALL READ
  ===================================================== */

  const markAllAsRead = () => {

    setNotifications(
      (previous) =>
        previous.map(
          (notification) => ({
            ...notification,
            read: true,
          })
        )
    );

  };


  /* =====================================================
     DELETE ONE
  ===================================================== */

  const deleteNotification = (id) => {

    setNotifications(
      (previous) =>
        previous.filter(
          (notification) =>
            notification.id !== id
        )
    );

  };


  /* =====================================================
     CLEAR ALL
  ===================================================== */

  const clearAll = () => {

    setNotifications([]);

  };


  /* =====================================================
     FILTER
  ===================================================== */

  const filteredNotifications =
    notifications.filter(
      (notification) => {

        if (filter === "all") {
          return true;
        }

        return (
          notification.type === filter
        );

      }
    );


  const unreadCount =
    notifications.filter(
      (notification) =>
        !notification.read
    ).length;


  return (

    <div className="notifications-page agent-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <section className="agent-page-header">

        <div>

          <div className="agent-eyebrow">

            <Bell size={14} />

            NOTIFICATIONS

          </div>


          <h1>
            Stay informed about your farm
          </h1>


          <p>
            Important updates from AgriSphere's
            climate, crop, market, government
            and AI intelligence systems.
          </p>

        </div>


        <div className="agent-header-icon">

          <Bell size={31} />

        </div>

      </section>


      {/* =================================================
          NOTIFICATION CONTROL BAR
      ================================================= */}

      <section className="notification-toolbar">


        <div className="notification-count">

          <div className="notification-count-icon">

            <Bell size={16} />

          </div>


          <div>

            <strong>
              {unreadCount}
            </strong>

            <span>
              unread notification
              {unreadCount !== 1
                ? "s"
                : ""}
            </span>

          </div>

        </div>


        <div className="notification-actions">


          {unreadCount > 0 && (

            <button
              type="button"
              className="notification-action-button"
              onClick={markAllAsRead}
            >

              <CheckCheck size={14} />

              Mark all as read

            </button>

          )}


          {notifications.length > 0 && (

            <button
              type="button"
              className="notification-action-button danger"
              onClick={clearAll}
            >

              <Trash2 size={14} />

              Clear all

            </button>

          )}

        </div>

      </section>


      {/* =================================================
          FILTER
      ================================================= */}

      <section className="notification-filter-bar">

        <div className="notification-filter-label">

          <Filter size={14} />

          Filter

        </div>


        <FilterButton
          label="All"
          value="all"
          active={filter === "all"}
          onClick={setFilter}
        />


        <FilterButton
          label="Climate"
          value="climate"
          active={filter === "climate"}
          onClick={setFilter}
        />


        <FilterButton
          label="Crop Health"
          value="crop"
          active={filter === "crop"}
          onClick={setFilter}
        />


        <FilterButton
          label="Market"
          value="market"
          active={filter === "market"}
          onClick={setFilter}
        />


        <FilterButton
          label="Government"
          value="government"
          active={filter === "government"}
          onClick={setFilter}
        />


        <FilterButton
          label="AI"
          value="recommendation"
          active={
            filter === "recommendation"
          }
          onClick={setFilter}
        />

      </section>


      {/* =================================================
          NOTIFICATION LIST
      ================================================= */}

      <section className="notification-list">


        {filteredNotifications.length === 0 ? (

          <EmptyNotifications />

        ) : (

          filteredNotifications.map(
            (notification) => (

              <NotificationCard
                key={notification.id}
                notification={notification}
                onRead={markAsRead}
                onDelete={
                  deleteNotification
                }
              />

            )
          )

        )}

      </section>

    </div>

  );
}


/* =========================================================
   FILTER BUTTON
========================================================= */

function FilterButton({
  label,
  value,
  active,
  onClick,
}) {

  return (

    <button
      type="button"
      className={`notification-filter-button ${
        active
          ? "active"
          : ""
      }`}
      onClick={() =>
        onClick(value)
      }
    >

      {label}

    </button>

  );

}


/* =========================================================
   NOTIFICATION CARD
========================================================= */

function NotificationCard({
  notification,
  onRead,
  onDelete,
}) {

  const Icon =
    notificationIcons[
      notification.type
    ] || Info;


  const priority =
    notification.priority ||
    "normal";


  return (

    <article
      className={`notification-card ${
        notification.read
          ? "read"
          : "unread"
      }`}
    >


      {/* ICON */}

      <div
        className={`notification-icon notification-${notification.type}`}
      >

        <Icon size={18} />

      </div>


      {/* CONTENT */}

      <div className="notification-content">


        <div className="notification-card-header">

          <div>

            <div className="notification-category">

              {getCategoryName(
                notification.type
              )}

            </div>


            <h3>
              {notification.title}
            </h3>

          </div>


          {!notification.read && (

            <span className="notification-new">

              NEW

            </span>

          )}

        </div>


        <p>
          {notification.message}
        </p>


        <div className="notification-card-footer">


          <span className="notification-time">

            <Clock3 size={12} />

            {notification.time}

          </span>


          {priority === "important" && (

            <span className="notification-important">

              <AlertTriangle size={12} />

              Important

            </span>

          )}


          <div className="notification-card-actions">


            {!notification.read && (

              <button
                type="button"
                onClick={() =>
                  onRead(
                    notification.id
                  )
                }
              >

                <Check size={13} />

                Mark read

              </button>

            )}


            <button
              type="button"
              className="delete"
              onClick={() =>
                onDelete(
                  notification.id
                )
              }
            >

              <Trash2 size={13} />

              Delete

            </button>

          </div>

        </div>

      </div>

    </article>

  );

}


/* =========================================================
   CATEGORY NAME
========================================================= */

function getCategoryName(type) {

  const names = {

    climate: "CLIMATE INTELLIGENCE",

    crop: "CROP HEALTH",

    market: "MARKET INTELLIGENCE",

    government: "GOVERNMENT SCHEMES",

    recommendation: "AI RECOMMENDATIONS",

  };


  return (
    names[type] ||
    "AGRISPHERE"
  );

}


/* =========================================================
   EMPTY STATE
========================================================= */

function EmptyNotifications() {

  return (

    <div className="notification-empty">

      <div className="notification-empty-icon">

        <CircleCheck size={25} />

      </div>


      <h3>
        You're all caught up
      </h3>


      <p>
        There are no notifications in
        this category right now.
      </p>

    </div>

  );

}


export default Notifications;