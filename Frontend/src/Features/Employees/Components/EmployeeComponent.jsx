import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import AllEmployees from "./AllEmployeesComponent";

export default function Employees() {
  const { theme } = useTheme();
  return (
    <main className={`${style.dashboardMain} ${!theme ? style.dark : ""}`}>
      <AllEmployees />
    </main>
  );
}
