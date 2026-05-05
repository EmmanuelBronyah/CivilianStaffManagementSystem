import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";
import OccurrenceData from "./OccurrenceDataComponent";

export default function ListEmployeeOccurrence(props) {
  const { theme } = useTheme();

  return (
    <div
      className={`${style.listEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          <button className={style.addOccurrence}>Add Occurrence</button>
        </div>

        <table>
          <thead>
            <tr>
              <th title="Service Number">Service Number</th>
              <th title="Grade">Grade</th>
              <th title="Authority">Authority</th>
              <th title="LevStep">LevStep</th>
              <th title="Monthly Salary">Monthly Salary</th>
              <th title="Annual Salary">Annual Salary</th>
              <th title="WEF Date">WEF Date</th>
              <th title="Date">Date</th>
              <th title="Reason">Reason</th>
            </tr>
          </thead>
          <tbody>
            <OccurrenceData
              serviceId={props.serviceId}
              setResponse={props.setResponse}
              editOccurrence={props.editOccurrence}
            />
          </tbody>
        </table>
      </div>
    </div>
  );
}
