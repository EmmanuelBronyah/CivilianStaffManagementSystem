import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import SampleEmployees from "./SampleEmployeesComponent";
import EmployeeDashboard from "./EmployeeDashboardComponent";
import { useRef, useState } from "react";

export default function Employees() {
  const [employeePage, setEmployeePage] = useState("Sample Employees");
  const serviceId = useRef("");

  const { theme } = useTheme();

  const displayEmployeeInfo = (employeeId) => {
    setEmployeePage("Employee Dashboard");
    serviceId.current = employeeId;
  };

  return (
    <main className={`${style.dashboardMain} ${!theme ? style.dark : ""}`}>
      {employeePage === "Sample Employees" && (
        <SampleEmployees displayEmployeeInfo={displayEmployeeInfo} />
      )}
      {employeePage === "Employee Dashboard" && (
        <EmployeeDashboard
          serviceId={serviceId.current}
          setEmployeePage={setEmployeePage}
        />
      )}
    </main>
  );
}
