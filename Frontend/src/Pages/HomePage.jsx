import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TEMP_TOKEN } from "../constants";
import Header from "../Components/HeaderComponent";
import SideBar from "../Components/SideBarComponent";
import Dashboard from "../Components/DashboardComponent";
import style from "../styles/pages/homepage.module.css";
import { useState } from "react";
import { useTheme } from "../context/ThemeContext";

function HomePage() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [displaySidebar, setDisplaySidebar] = useState(false);
  const { theme } = useTheme();

  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem(TEMP_TOKEN);
    localStorage.removeItem("otpTaskId");
    localStorage.removeItem("otp_expiry");
  }, []);

  const navigateToLogoutPage = () => {
    navigate("/auth/logout");
  };

  const toggleSidebar = () => {
    setDisplaySidebar((prevState) => !prevState);
  };

  return (
    <div className={`${style.homePage} ${!theme && style.dark}`}>
      <div className={style.wrapper}>
        <SideBar
          activePage={activePage}
          setActivePage={setActivePage}
          toggleSidebar={toggleSidebar}
          displaySidebar={displaySidebar}
        />
        <div className={style.headerMainContainer}>
          <Header activePage={activePage} toggleSidebar={toggleSidebar} />
          {activePage === "Dashboard" && <Dashboard />}
        </div>
      </div>
    </div>
  );
}

{
  /* <button onClick={navigateToLogoutPage}>Logout</button>; */
}
export default HomePage;
