import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function IdentityInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Identity</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Identity"} />
      </div>
    </>
  );
}
