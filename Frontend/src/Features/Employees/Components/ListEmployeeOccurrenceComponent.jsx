import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";
import OccurrenceData from "./OccurrenceDataComponent";
import { useState } from "react";

export default function ListEmployeeOccurrence(props) {
  const [loading, setLoading] = useState(true);
  const { theme } = useTheme();

  return (
    <div
      className={`${style.listEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          {loading ? (
            <BaseSkeleton width={170} height={39} />
          ) : (
            <button className={style.addOccurrence}>Add Occurrence</button>
          )}
        </div>

        <div>
          <table>
            {loading ? (
              <BaseSkeleton height={38} />
            ) : (
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
            )}

            <tbody>
              <OccurrenceData
                serviceId={props.serviceId}
                setResponse={props.setResponse}
                editOccurrence={props.editOccurrence}
                loading={loading}
                setLoading={setLoading}
              />
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
