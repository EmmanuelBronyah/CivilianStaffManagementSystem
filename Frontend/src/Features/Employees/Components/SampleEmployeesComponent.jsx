import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import EmployeeData from "./EmployeeDataComponent";
import { useState } from "react";

export default function SampleEmployees({ displayEmployeeInfo, setResponse }) {
  const [loading, setLoading] = useState(true);

  const { theme } = useTheme();

  return (
    <>
      <div
        className={`${style.listEmployeesContainer} ${!theme ? style.dark : ""}`}
      >
        <div className={style.titleAndButtonsContainer}>
          <div className={style.employeeTitleAndTwoButtonsContainer}>
            <p className={style.employeesTitle}>Sample Employees</p>
            <div className={style.twoButtonsContainer}>
              <button className={style.newEmployeeButton}>New Employee</button>
              <button className={style.advancedSearchButton}>
                Advanced Search
              </button>
            </div>
          </div>
          <button className={style.applyOccurrenceButton}>
            Apply Occurrence
          </button>
        </div>
        <div className={style.employeeListContainer}>
          <table>
            <thead>
              <tr>
                <th title="Service Number">Service Number</th>
                <th title="Name">Name</th>
                <th title="Unit">Unit</th>
                <th title="Grade">Grade</th>
                <th title="Category">Category</th>
                <th title="Appointment Date">Appointment Date</th>
                <th title="Status">Status</th>
              </tr>
            </thead>

            <tbody>
              <EmployeeData
                loading={loading}
                setLoading={setLoading}
                setResponse={setResponse}
                displayEmployeeInfo={displayEmployeeInfo}
              />
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
