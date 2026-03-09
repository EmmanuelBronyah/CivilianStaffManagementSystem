import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TEMP_TOKEN } from "../constants";
import Header from "../Components/HeaderComponent";
import SideBar from "../Components/SideBarComponent";
import style from "../styles/pages/dashboard.module.css";

function Dashboard() {
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
    <div className={style.dashboard}>
      <SideBar className={style.sideBar} />
      <div className={style.headerMainContainer}>
        <Header className={style.header} />
        <main>Main Area</main>
      </div>
    </div>
  );
}

{
  /* <button onClick={navigateToLogoutPage}>Logout</button> */
}
export default Dashboard;
