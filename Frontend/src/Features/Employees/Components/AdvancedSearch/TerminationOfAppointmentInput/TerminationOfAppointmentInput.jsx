import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function TerminationOfAppointmentInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Termination Of Appointment</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Termination Of Appointment"} />
      </div>
    </>
  );
}
