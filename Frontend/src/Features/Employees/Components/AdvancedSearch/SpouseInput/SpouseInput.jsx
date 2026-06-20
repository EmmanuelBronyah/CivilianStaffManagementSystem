import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function SpouseInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Spouse</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Spouse"} />
      </div>
    </>
  );
}
