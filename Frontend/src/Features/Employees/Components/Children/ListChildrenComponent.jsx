import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import ChildrenData from "./ChildrenDataComponent";
import { useState } from "react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function ListChildren() {
  const [loading, setLoading] = useState(true);
  const { theme } = useTheme();
  const { setResponse } = useOutletContext();
  const navigate = useNavigate();
  const { serviceId } = useParams();

  return (
    <div
      className={`${style.listEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          {loading ? (
            <BaseSkeleton width={170} height={39} />
          ) : (
            <button
              className={style.addOccurrence}
              onClick={() =>
                navigate(`/home/employees/${serviceId}/children/add`)
              }
            >
              Add Child
            </button>
          )}
        </div>

        <div>
          <table>
            {loading ? (
              <BaseSkeleton height={38} />
            ) : (
              <thead>
                <tr>
                  <th title="Child's Name">Child's Name</th>
                  <th title="Date Of Birth">Date Of Birth</th>
                  <th title="Gender">Gender</th>
                  <th title="Name Of Other Parent">Name Of Other Parent</th>
                  <th title="Authority">Authority</th>
                </tr>
              </thead>
            )}

            <tbody>
              <ChildrenData
                setResponse={setResponse}
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
