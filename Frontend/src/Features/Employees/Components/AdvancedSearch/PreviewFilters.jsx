import style from "../../../../styles/components/advancedsearch.module.css";
import { displayLabels, displayRange } from "./constants";

export default function PreviewFilters({ formData }) {
  function transformData(formData) {
    const transformedData = {};

    for (const [record, recordValues] of Object.entries(formData)) {
      for (const [label, labelValue] of Object.entries(recordValues)) {
        // 1. Primitive value
        if (labelValue === null || typeof labelValue !== "object") {
          if (labelValue === null || labelValue === "") {
            continue;
          }

          transformedData[record] = {
            ...transformedData[record],
            [displayLabels[record][label]]: labelValue,
          };

          continue;
        }

        // 2. React Select option
        if ("value" in labelValue && "label" in labelValue) {
          if (labelValue.value === null || labelValue.value === "") {
            continue;
          }

          transformedData[record] = {
            ...transformedData[record],
            [displayLabels[record][label]]: labelValue.label,
          };

          continue;
        }

        // 3. Range object
        const [rangeKey, rangeValue] = Object.entries(labelValue)[0];

        if (typeof rangeValue !== "object") {
          if (rangeValue === "") {
            continue;
          }

          transformedData[record] = {
            ...transformedData[record],
            [displayLabels[record][label]]:
              `${displayRange[rangeKey]}: ${rangeValue}`,
          };

          continue;
        }

        // 4. Between range
        const { from, to } = rangeValue;

        // Skip the field if both values are empty
        if (from === "" && to === "") {
          continue;
        }

        transformedData[record] = {
          ...transformedData[record],
          [displayLabels[record][label]]:
            `${displayRange[rangeKey]}: ${from || ""} to ${to || ""}`,
        };
      }
    }

    return transformedData;
  }

  const transformedData = transformData(formData);

  return (
    <div className={style.previewFilters}>
      {Object.entries(transformedData).map(([record, fields]) => (
        <div key={record} className={style.singlePreviewContainer}>
          <div className={style.previewRecordTitle}>
            <i>
              <b>{record}</b>
            </i>
          </div>
          <div className={style.fieldValueContainer}>
            {Object.entries(fields).map(([field, value]) => (
              <div key={field} className={style.fieldAndValue}>
                <div className={style.fieldContainer}>
                  <i>
                    <b className={style.field}>{field}</b>
                  </i>
                </div>
                <b className={style.value}>{value}</b>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
