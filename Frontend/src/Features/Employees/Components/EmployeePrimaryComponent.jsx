import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";

export default function EmployeePrimary({ data }) {
  const { theme } = useTheme();
  return (
    <div
      className={`${style.employeePrimary} ${!theme ? style.dark : ""}`}
    ></div>
  );
}
