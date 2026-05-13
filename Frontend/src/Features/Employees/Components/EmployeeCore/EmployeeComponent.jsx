import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useState, useEffect } from "react";
import Notification from "../../../../Components/Common/NotificationComponent";
import { Outlet } from "react-router-dom";

export default function Employees() {
  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);

  const { theme } = useTheme();

  useEffect(() => {
    if (!response) return;

    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [response]);

  return (
    <main className={`${style.dashboardMain} ${!theme ? style.dark : ""}`}>
      <Outlet context={{ setResponse }} />
      <Notification isVisible={visible} response={response} />
    </main>
  );
}
