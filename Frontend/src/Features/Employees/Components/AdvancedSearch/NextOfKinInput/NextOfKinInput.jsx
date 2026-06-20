import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function NextOfKinInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Emergency | Next Of Kin</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Next Of Kin"} />
      </div>
    </>
  );
}
