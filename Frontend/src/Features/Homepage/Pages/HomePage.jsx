import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TEMP_TOKEN } from "../../../constants";
import Header from "../../../Components/Layouts/HeaderComponent";
import SideBar from "../../../Components/Layouts/SideBarComponent";
import style from "../../../styles/pages/homepage.module.css";
import { useState } from "react";
import { useTheme } from "../../../Context/ThemeContext";
import Notification from "../../../Components/Common/NotificationComponent";
import { Outlet } from "react-router-dom";

function HomePage() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [open, setOpen] = useState(false);
  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);

  const { theme } = useTheme();

  const navigate = useNavigate();

  useEffect(() => {
    if (!response) return;

    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [response]);

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
          <Header
            activePage={activePage}
            setOpen={setOpen}
            setResponse={setResponse}
          />
          <Outlet />
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </div>
  );
}

{
  /* <button onClick={navigateToLogoutPage}>Logout</button>; */
}
export default HomePage;
