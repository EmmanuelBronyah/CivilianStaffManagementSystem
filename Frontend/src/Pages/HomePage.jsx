import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TEMP_TOKEN } from "../constants";
import Header from "../Components/HeaderComponent";
import SideBar from "../Components/SideBarComponent";
import Dashboard from "../Components/DashboardComponent";
import Users from "../Components/UsersComponent";
import style from "../styles/pages/homepage.module.css";
import { useState } from "react";
import { useTheme } from "../context/ThemeContext";

function HomePage() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [open, setOpen] = useState(false);

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

  return (
    <div className={`${style.homePage} ${!theme && style.dark}`}>
      <div className={style.wrapper}>
        <SideBar
          activePage={activePage}
          setActivePage={setActivePage}
          open={open}
          setOpen={setOpen}
        />
        <div className={style.headerMainContainer}>
          <Header activePage={activePage} setOpen={setOpen} />
          {activePage === "Dashboard" && <Dashboard />}
          {activePage === "Users" && <Users />}
        </div>
      </div>
    </div>
  );
}

{
  /* <button onClick={navigateToLogoutPage}>Logout</button>; */
}
export default HomePage;
