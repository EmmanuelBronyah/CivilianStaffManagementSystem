import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import NextOfKinData from "./NextOfKinDataComponent";
import { useState } from "react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function ListNextOfKin() {
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
                navigate(`/home/employees/${serviceId}/nextOfKin/add`)
              }
            >
              Add Next Of Kin
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
                  <th title="Name">Name</th>
                  <th title="Relation">Relation</th>
                  <th title="E-mail">E-mail</th>
                  <th title="Address">Address</th>
                  <th title="Mobile">Mobile</th>
                  <th title="E-contact">E-contact</th>
                </tr>
              </thead>
            )}

            <tbody>
              <NextOfKinData
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
