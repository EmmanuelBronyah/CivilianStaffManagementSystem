import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import SampleEmployees from "./SampleEmployeesComponent";
import EmployeeDashboard from "./EmployeeDashboardComponent";
import { useRef, useState, useEffect } from "react";
import Notification from "../../../Components/Common/NotificationComponent";

export default function Employees() {
  const [employeePage, setEmployeePage] = useState("Sample Employees");
  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);
  const serviceId = useRef("");

  const { theme } = useTheme();

  useEffect(() => {
    if (!response) return;

    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [response]);

  const displayEmployeeInfo = (employeeId) => {
    setEmployeePage("Employee Dashboard");
    serviceId.current = employeeId;
  };

  return (
    <main className={`${style.dashboardMain} ${!theme ? style.dark : ""}`}>
      {employeePage === "Sample Employees" && (
        <SampleEmployees
          displayEmployeeInfo={displayEmployeeInfo}
          setResponse={setResponse}
        />
      )}
      {employeePage === "Employee Dashboard" && (
        <EmployeeDashboard
          serviceId={serviceId.current}
          setEmployeePage={setEmployeePage}
          setResponse={setResponse}
        />
      )}
      <Notification isVisible={visible} response={response} />
    </main>
  );
}
