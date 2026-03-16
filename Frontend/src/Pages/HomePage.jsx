import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TEMP_TOKEN } from "../constants";
import Header from "../Components/HeaderComponent";
import SideBar from "../Components/SideBarComponent";
import Dashboard from "../Components/DashboardComponent";
import style from "../styles/pages/homepage.module.css";
import { useState } from "react";

function HomePage() {
  const [activePage, setActivePage] = useState("Dashboard");

  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem(TEMP_TOKEN);
    localStorage.removeItem("otpTaskId");
    localStorage.removeItem("otp_expiry");
  }, []);

  const navigateToLogoutPage = () => {
    navigate("/auth/logout");
  };

  return (
    <div className={style.homePage}>
      <SideBar activePage={activePage} setActivePage={setActivePage} />
      <div className={style.headerMainContainer}>
        <Header activePage={activePage} />
        {activePage === "Dashboard" && <Dashboard />}
      </div>
      {/* <button onClick={navigateToLogoutPage}>Logout</button>; */}
    </div>
  );
}

export default HomePage;
