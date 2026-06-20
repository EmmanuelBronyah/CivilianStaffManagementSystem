import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function OccurrenceInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Occurrence</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Occurrence"} />
      </div>
    </>
  );
}
