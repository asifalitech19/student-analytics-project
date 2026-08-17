// import { useEffect, useState } from "react";

// const API_BASE_URL = "http://127.0.0.1:8000";

// const initialForm = {
//   age: "",
//   gender: "",
//   relationship_status: "",
//   living_arrangement: "",
//   health_issues: "",
//   physical_disability: "",
//   admission_year: "",
//   hsc_year: "",
//   scholarship: "",
//   english_proficiency: "",
//   study_hours: "",
//   study_sessions: "",
//   social_media_hours: "",
//   skill_development_hours: "",
// };

// function PredictionForm() {
//   const [form, setForm] = useState(initialForm);

//   const [options, setOptions] = useState({
//     categorical: {},
//     numerical_ranges: {},
//   });

//   const [loadingOptions, setLoadingOptions] = useState(true);
//   const [predicting, setPredicting] = useState(false);

//   const [prediction, setPrediction] = useState(null);
//   const [error, setError] = useState("");

//   // ============================================================
//   // LOAD OPTIONS
//   // ============================================================

//   useEffect(() => {
//     const loadOptions = async () => {
//       try {
//         setLoadingOptions(true);

//         const response = await fetch(
//           `${API_BASE_URL}/api/predict/options`
//         );

//         if (!response.ok) {
//           throw new Error("Unable to load prediction options.");
//         }

//         const data = await response.json();

//         setOptions(
//           data.options || {
//             categorical: {},
//             numerical_ranges: {},
//           }
//         );
//       } catch (err) {
//         setError(
//           err.message ||
//             "Unable to load prediction options."
//         );
//       } finally {
//         setLoadingOptions(false);
//       }
//     };

//     loadOptions();
//   }, []);

//   // ============================================================
//   // HANDLE INPUT
//   // ============================================================

//   const handleChange = (event) => {
//     const { name, value } = event.target;

//     setForm((previous) => ({
//       ...previous,
//       [name]: value,
//     }));

//     setError("");

//     // Clear previous prediction when user changes input
//     setPrediction(null);
//   };

//   // ============================================================
//   // VALIDATE FORM
//   // ============================================================

//   const validateForm = () => {
//     const requiredFields = Object.keys(form);

//     for (const field of requiredFields) {
//       const value = form[field];

//       if (
//         value === null ||
//         value === undefined ||
//         String(value).trim() === ""
//       ) {
//         return `Please complete: ${getLabel(field)}`;
//       }
//     }

//     const age = Number(form.age);

//     if (age < 15 || age > 80) {
//       return "Age must be between 15 and 80.";
//     }

//     const admissionYear = Number(
//       form.admission_year
//     );

//     if (
//       admissionYear < 1990 ||
//       admissionYear > 2035
//     ) {
//       return "University Admission Year must be between 1990 and 2035.";
//     }

//     const hscYear = Number(form.hsc_year);

//     if (
//       hscYear < 1990 ||
//       hscYear > 2035
//     ) {
//       return "H.S.C Passing Year must be between 1990 and 2035.";
//     }

//     const studyHours = Number(
//       form.study_hours
//     );

//     if (
//       studyHours < 0 ||
//       studyHours > 24
//     ) {
//       return "Daily Study Hours must be between 0 and 24.";
//     }

//     const sessions = Number(
//       form.study_sessions
//     );

//     if (
//       sessions < 0 ||
//       sessions > 30
//     ) {
//       return "Study Sessions must be between 0 and 30.";
//     }

//     const socialHours = Number(
//       form.social_media_hours
//     );

//     if (
//       socialHours < 0 ||
//       socialHours > 24
//     ) {
//       return "Social Media Hours must be between 0 and 24.";
//     }

//     const skillHours = Number(
//       form.skill_development_hours
//     );

//     if (
//       skillHours < 0 ||
//       skillHours > 24
//     ) {
//       return "Skill Development Hours must be between 0 and 24.";
//     }

//     return "";
//   };

//   // ============================================================
//   // SUBMIT PREDICTION
//   // ============================================================

//   const handleSubmit = async (event) => {
//     event.preventDefault();

//     setError("");
//     setPrediction(null);

//     const validationError = validateForm();

//     if (validationError) {
//       setError(validationError);
//       return;
//     }

//     try {
//       setPredicting(true);

//       const payload = {
//         age: Number(form.age),

//         gender: form.gender,

//         relationship_status:
//           form.relationship_status,

//         living_arrangement:
//           form.living_arrangement,

//         health_issues:
//           form.health_issues,

//         physical_disability:
//           form.physical_disability,

//         admission_year:
//           Number(form.admission_year),

//         hsc_year:
//           Number(form.hsc_year),

//         scholarship:
//           form.scholarship,

//         english_proficiency:
//           form.english_proficiency,

//         study_hours:
//           Number(form.study_hours),

//         study_sessions:
//           Number(form.study_sessions),

//         social_media_hours:
//           Number(form.social_media_hours),

//         skill_development_hours:
//           Number(
//             form.skill_development_hours
//           ),
//       };

//       const response = await fetch(
//         `${API_BASE_URL}/api/predict/`,
//         {
//           method: "POST",

//           headers: {
//             "Content-Type": "application/json",
//           },

//           body: JSON.stringify(payload),
//         }
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(
//           data.detail ||
//             "Prediction request failed."
//         );
//       }

//       const predictedCgpa =
//         data?.prediction?.predicted_cgpa;

//       if (
//         predictedCgpa === undefined ||
//         predictedCgpa === null
//       ) {
//         throw new Error(
//           "The server returned an invalid prediction."
//         );
//       }

//       setPrediction(
//         Number(predictedCgpa).toFixed(2)
//       );
//     } catch (err) {
//       setError(
//         err.message ||
//           "Unable to generate prediction."
//       );
//     } finally {
//       setPredicting(false);
//     }
//   };

//   // ============================================================
//   // RESET
//   // ============================================================

//   const handleReset = () => {
//     setForm(initialForm);
//     setPrediction(null);
//     setError("");
//   };

//   // ============================================================
//   // LABEL HELPER
//   // ============================================================

//   const getLabel = (field) => {
//     const labels = {
//       age: "Age",
//       gender: "Gender",
//       relationship_status:
//         "Relationship Status",
//       living_arrangement:
//         "Living Arrangement",
//       health_issues:
//         "Health Issues",
//       physical_disability:
//         "Physical Disability",
//       admission_year:
//         "University Admission Year",
//       hsc_year:
//         "H.S.C Passing Year",
//       scholarship:
//         "Meritorious Scholarship",
//       english_proficiency:
//         "English Proficiency",
//       study_hours:
//         "Daily Study Hours",
//       study_sessions:
//         "Study Sessions Per Day",
//       social_media_hours:
//         "Daily Social Media Hours",
//       skill_development_hours:
//         "Daily Skill Development Hours",
//     };

//     return labels[field] || field;
//   };

//   // ============================================================
//   // OPTIONS HELPER
//   // ============================================================

//   const getOptions = (field) => {
//     const map = {
//       gender:
//         "Gender",

//       relationship_status:
//         "What is your relationship status?",

//       living_arrangement:
//         "With whom you are living with?",

//       health_issues:
//         "Do you have any health issues?",

//       physical_disability:
//         "Do you have any physical disabilities?",

//       scholarship:
//         "Do you have meritorious scholarship ?",

//       english_proficiency:
//         "Status of your English language proficiency",
//     };

//     return (
//       options?.categorical?.[
//         map[field]
//       ] || []
//     );
//   };

//   // ============================================================
//   // REUSABLE SELECT
//   // ============================================================

//   const renderSelect = (
//     name,
//     optionsList
//   ) => {
//     return (
//       <div className="space-y-2">
//         <label className="block text-sm font-medium text-slate-700">
//           {getLabel(name)}
//         </label>

//         <select
//           name={name}
//           value={form[name]}
//           onChange={handleChange}
//           disabled={
//             loadingOptions || predicting
//           }
//           className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:cursor-not-allowed disabled:bg-slate-100"
//         >
//           <option value="">
//             Select {getLabel(name)}
//           </option>

//           {optionsList.map(
//             (option) => (
//               <option
//                 key={option}
//                 value={option}
//               >
//                 {option}
//               </option>
//             )
//           )}
//         </select>
//       </div>
//     );
//   };

//   // ============================================================
//   // RENDER
//   // ============================================================

//   return (
//     <div className="w-full">
//       <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
//         {/* Header */}

//         <div className="mb-6">
//           <h2 className="text-2xl font-bold tracking-tight text-slate-900">
//             CGPA Prediction
//           </h2>

//           <p className="mt-1 text-sm text-slate-500">
//             Enter the student's information to
//             estimate the current CGPA.
//           </p>
//         </div>

//         {/* Error */}

//         {error && (
//           <div className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
//             {error}
//           </div>
//         )}

//         {/* Loading */}

//         {loadingOptions && (
//           <div className="mb-5 rounded-xl border border-indigo-100 bg-indigo-50 px-4 py-3 text-sm text-indigo-700">
//             Loading prediction options...
//           </div>
//         )}

//         {/* Form */}

//         <form
//           onSubmit={handleSubmit}
//           className="space-y-8"
//         >
//           {/* =====================================================
//               DEMOGRAPHIC
//           ====================================================== */}

//           <section>
//             <h3 className="mb-4 text-base font-semibold text-slate-900">
//               Student Information
//             </h3>

//             <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
//               {/* Age */}

//               <div className="space-y-2">
//                 <label className="block text-sm font-medium text-slate-700">
//                   Age
//                 </label>

//                 <input
//                   type="number"
//                   name="age"
//                   min="15"
//                   max="80"
//                   value={form.age}
//                   onChange={handleChange}
//                   placeholder="e.g. 21"
//                   disabled={predicting}
//                   className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100"
//                 />
//               </div>

//               {renderSelect(
//                 "gender",
//                 getOptions("gender")
//               )}

//               {renderSelect(
//                 "relationship_status",
//                 getOptions(
//                   "relationship_status"
//                 )
//               )}

//               {renderSelect(
//                 "living_arrangement",
//                 getOptions(
//                   "living_arrangement"
//                 )
//               )}

//               {renderSelect(
//                 "health_issues",
//                 getOptions(
//                   "health_issues"
//                 )
//               )}

//               {renderSelect(
//                 "physical_disability",
//                 getOptions(
//                   "physical_disability"
//                 )
//               )}
//             </div>
//           </section>

//           {/* =====================================================
//               ACADEMIC
//           ====================================================== */}

//           <section>
//             <h3 className="mb-4 text-base font-semibold text-slate-900">
//               Academic Information
//             </h3>

//             <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
//               {/* Admission Year */}

//               <div className="space-y-2">
//                 <label className="block text-sm font-medium text-slate-700">
//                   University Admission Year
//                 </label>

//                 <input
//                   type="number"
//                   name="admission_year"
//                   min="1990"
//                   max="2035"
//                   value={
//                     form.admission_year
//                   }
//                   onChange={handleChange}
//                   placeholder="e.g. 2022"
//                   disabled={predicting}
//                   className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100"
//                 />
//               </div>

//               {/* HSC Year */}

//               <div className="space-y-2">
//                 <label className="block text-sm font-medium text-slate-700">
//                   H.S.C Passing Year
//                 </label>

//                 <input
//                   type="number"
//                   name="hsc_year"
//                   min="1990"
//                   max="2035"
//                   value={form.hsc_year}
//                   onChange={handleChange}
//                   placeholder="e.g. 2020"
//                   disabled={predicting}
//                   className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100"
//                 />
//               </div>

//               {renderSelect(
//                 "scholarship",
//                 getOptions(
//                   "scholarship"
//                 )
//               )}

//               {renderSelect(
//                 "english_proficiency",
//                 getOptions(
//                   "english_proficiency"
//                 )
//               )}
//             </div>
//           </section>

//           {/* =====================================================
//               STUDY BEHAVIOR
//           ====================================================== */}

//           <section>
//             <h3 className="mb-4 text-base font-semibold text-slate-900">
//               Study & Daily Behavior
//             </h3>

//             <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
//               {/* Study Hours */}

//               <div className="space-y-2">
//                 <label className="block text-sm font-medium text-slate-700">
//                   Daily Study Hours
//                 </label>

//                 <input
//                   type="number"
//                   name="study_hours"
//                   min="0"
//                   max="24"
//                   step="0.5"
//                   value={form.study_hours}
//                   onChange={handleChange}
//                   placeholder="e.g. 5"
//                   disabled={predicting}
//                   className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100"
//                 />
//               </div>

//               {/* Study Sessions */}

//               <div className="space-y-2">
//                 <label className="block text-sm font-medium text-slate-700">
//                   Study Sessions Per Day
//                 </label>

//                 <input
//                   type="number"
//                   name="study_sessions"
//                   min="0"
//                   max="30"
//                   step="1"
//                   value={
//                     form.study_sessions
//                   }
//                   onChange={handleChange}
//                   placeholder="e.g. 2"
//                   disabled={predicting}
//                   className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100"
//                 />
//               </div>

//               {/* Social Media */}

//               <div className="space-y-2">
//                 <label className="block text-sm font-medium text-slate-700">
//                   Daily Social Media Hours
//                 </label>

//                 <input
//                   type="number"
//                   name="social_media_hours"
//                   min="0"
//                   max="24"
//                   step="0.5"
//                   value={
//                     form.social_media_hours
//                   }
//                   onChange={handleChange}
//                   placeholder="e.g. 3"
//                   disabled={predicting}
//                   className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100"
//                 />
//               </div>

//               {/* Skill Development */}

//               <div className="space-y-2">
//                 <label className="block text-sm font-medium text-slate-700">
//                   Daily Skill Development Hours
//                 </label>

//                 <input
//                   type="number"
//                   name="skill_development_hours"
//                   min="0"
//                   max="24"
//                   step="0.5"
//                   value={
//                     form.skill_development_hours
//                   }
//                   onChange={handleChange}
//                   placeholder="e.g. 2"
//                   disabled={predicting}
//                   className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100"
//                 />
//               </div>
//             </div>
//           </section>

//           {/* =====================================================
//               ACTIONS
//           ====================================================== */}

//           <div className="flex flex-col gap-3 border-t border-slate-100 pt-6 sm:flex-row">
//             <button
//               type="submit"
//               disabled={
//                 predicting ||
//                 loadingOptions
//               }
//               className="flex-1 rounded-xl bg-indigo-600 px-5 py-3 font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
//             >
//               {predicting
//                 ? "Predicting..."
//                 : "Predict CGPA"}
//             </button>

//             <button
//               type="button"
//               onClick={handleReset}
//               disabled={predicting}
//               className="rounded-xl border border-slate-200 bg-white px-5 py-3 font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
//             >
//               Reset
//             </button>
//           </div>
//         </form>
//       </div>

//       {/* ==========================================================
//           RESULT
//       =========================================================== */}

//       {prediction !== null && (
//         <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
//           <p className="text-sm font-medium text-slate-500">
//             Predicted CGPA
//           </p>

//           <div className="mt-3 text-6xl font-bold tracking-tight text-indigo-600">
//             {prediction}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default PredictionForm;






import React, { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

const initialForm = {
  age: "",
  gender: "",
  relationship_status: "",
  living_arrangement: "",
  health_issues: "",
  physical_disability: "",
  admission_year: "",
  hsc_year: "",
  scholarship: "",
  english_proficiency: "",
  study_hours: "",
  study_sessions: "",
  social_media_hours: "",
  skill_development_hours: "",
};

function PremiumPredictionForm() {
  const [form, setForm] = useState(initialForm);
  const [options, setOptions] = useState({ categorical: {}, numerical_ranges: {} });
  const [loadingOptions, setLoadingOptions] = useState(true);
  const [predicting, setPredicting] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");

  // ============================================================
  // LOAD OPTIONS (Logic Unchanged)
  // ============================================================
  useEffect(() => {
    const loadOptions = async () => {
      try {
        setLoadingOptions(true);
        const response = await fetch(`${API_BASE_URL}/api/predict/options`);
        if (!response.ok) throw new Error("Unable to load prediction options.");
        const data = await response.json();
        setOptions(data.options || { categorical: {}, numerical_ranges: {} });
      } catch (err) {
        setError(err.message || "Unable to load prediction options.");
      } finally {
        setLoadingOptions(false);
      }
    };
    loadOptions();
  }, []);

  // ============================================================
  // HANDLE INPUT (Logic Unchanged)
  // ============================================================
  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    setError("");
    setPrediction(null);
  };

  // ============================================================
  // VALIDATE FORM (Logic Unchanged)
  // ============================================================
  const validateForm = () => {
    const requiredFields = Object.keys(form);
    for (const field of requiredFields) {
      const value = form[field];
      if (value === null || value === undefined || String(value).trim() === "") {
        return `Please complete: ${getLabel(field)}`;
      }
    }
    const age = Number(form.age);
    if (age < 15 || age > 80) return "Age must be between 15 and 80.";
    const admissionYear = Number(form.admission_year);
    if (admissionYear < 1990 || admissionYear > 2035) return "Admission Year must be between 1990 and 2035.";
    const hscYear = Number(form.hsc_year);
    if (hscYear < 1990 || hscYear > 2035) return "H.S.C Passing Year must be between 1990 and 2035.";
    const studyHours = Number(form.study_hours);
    if (studyHours < 0 || studyHours > 24) return "Daily Study Hours must be between 0 and 24.";
    const sessions = Number(form.study_sessions);
    if (sessions < 0 || sessions > 30) return "Study Sessions must be between 0 and 30.";
    const socialHours = Number(form.social_media_hours);
    if (socialHours < 0 || socialHours > 24) return "Social Media Hours must be between 0 and 24.";
    const skillHours = Number(form.skill_development_hours);
    if (skillHours < 0 || skillHours > 24) return "Skill Development Hours must be between 0 and 24.";
    return "";
  };

  // ============================================================
  // SUBMIT PREDICTION (Logic Unchanged)
  // ============================================================
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setPrediction(null);
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }
    try {
      setPredicting(true);
      const payload = {
        age: Number(form.age),
        gender: form.gender,
        relationship_status: form.relationship_status,
        living_arrangement: form.living_arrangement,
        health_issues: form.health_issues,
        physical_disability: form.physical_disability,
        admission_year: Number(form.admission_year),
        hsc_year: Number(form.hsc_year),
        scholarship: form.scholarship,
        english_proficiency: form.english_proficiency,
        study_hours: Number(form.study_hours),
        study_sessions: Number(form.study_sessions),
        social_media_hours: Number(form.social_media_hours),
        skill_development_hours: Number(form.skill_development_hours),
      };

      const response = await fetch(`${API_BASE_URL}/api/predict/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Prediction request failed.");
      
      const predictedCgpa = data?.prediction?.predicted_cgpa;
      if (predictedCgpa === undefined || predictedCgpa === null) {
        throw new Error("The server returned an invalid prediction.");
      }
      setPrediction(Number(predictedCgpa).toFixed(2));
    } catch (err) {
      setError(err.message || "Unable to generate prediction.");
    } finally {
      setPredicting(false);
    }
  };

  const handleReset = () => {
    setForm(initialForm);
    setPrediction(null);
    setError("");
  };

  // ============================================================
  // HELPERS (Logic Unchanged)
  // ============================================================
  const getLabel = (field) => {
    const labels = {
      age: "Age", gender: "Gender", relationship_status: "Relationship Status",
      living_arrangement: "Living Arrangement", health_issues: "Health Issues",
      physical_disability: "Physical Disability", admission_year: "University Admission Year",
      hsc_year: "H.S.C Passing Year", scholarship: "Meritorious Scholarship",
      english_proficiency: "English Proficiency", study_hours: "Daily Study Hours",
      study_sessions: "Study Sessions Per Day", social_media_hours: "Daily Social Media Hours",
      skill_development_hours: "Daily Skill Development Hours",
    };
    return labels[field] || field;
  };

  const getOptions = (field) => {
    const map = {
      gender: "Gender", relationship_status: "What is your relationship status?",
      living_arrangement: "With whom you are living with?", health_issues: "Do you have any health issues?",
      physical_disability: "Do you have any physical disabilities?", scholarship: "Do you have meritorious scholarship ?",
      english_proficiency: "Status of your English language proficiency",
    };
    return options?.categorical?.[map[field]] || [];
  };

  // ============================================================
  // UPGRADED REUSABLE SELECT
  // ============================================================
  const renderSelect = (name, optionsList) => (
    <div className="space-y-1.5">
      <label className="block text-sm font-semibold text-slate-700">{getLabel(name)}</label>
      <div className="relative">
        <select
          name={name}
          value={form[name]}
          onChange={handleChange}
          disabled={loadingOptions || predicting}
          className="w-full appearance-none rounded-xl border border-slate-200 bg-slate-50/50 px-4 py-3.5 text-sm text-slate-800 outline-none transition-all focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <option value="" disabled>Select {getLabel(name)}</option>
          {optionsList.map((option) => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        {/* Custom Dropdown Arrow */}
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-400">
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  );

  // ============================================================
  // UPGRADED REUSABLE INPUT
  // ============================================================
  const renderInput = (name, type = "number", min, max, step, placeholder) => (
    <div className="space-y-1.5">
      <label className="block text-sm font-semibold text-slate-700">{getLabel(name)}</label>
      <input
        type={type}
        name={name}
        min={min} max={max} step={step}
        value={form[name]}
        onChange={handleChange}
        placeholder={placeholder}
        disabled={predicting}
        className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-4 py-3.5 text-sm text-slate-800 outline-none transition-all focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10 disabled:cursor-not-allowed disabled:opacity-60"
      />
    </div>
  );

  // ============================================================
  // RENDER
  // ============================================================
  return (
    <div className="mx-auto w-full max-w-4xl space-y-8">
      
      {/* MAIN CARD */}
      <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-xl shadow-slate-200/40">
        
        {/* HEADER SECTION */}
        <div className="relative border-b border-slate-100 bg-slate-50 p-8 sm:p-10">
          <div className="absolute top-0 left-0 h-1 w-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />
          <h2 className="text-3xl font-extrabold tracking-tight text-slate-900">
            <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              AI Powered
            </span>{" "}
            CGPA Predictor
          </h2>
          <p className="mt-2 text-base text-slate-500">
            Enter the student's demographic, academic, and behavioral data to estimate their current CGPA with high accuracy.
          </p>
        </div>

        <div className="p-8 sm:p-10">
          {error && (
            <div className="mb-8 flex items-center gap-3 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm font-medium text-rose-700 animate-in fade-in slide-in-from-top-2">
              <svg className="h-5 w-5 shrink-0 text-rose-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              {error}
            </div>
          )}

          {loadingOptions && (
            <div className="mb-8 flex items-center gap-3 rounded-2xl border border-indigo-100 bg-indigo-50/50 p-4 text-sm font-medium text-indigo-700">
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-indigo-600 border-t-transparent"></div>
              Initializing AI models and loading options...
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-10">
            
            {/* DEMOGRAPHIC SECTION */}
            <section className="rounded-2xl border border-slate-100 bg-white p-6 shadow-sm ring-1 ring-slate-900/5">
              <div className="mb-5 flex items-center gap-2 border-b border-slate-100 pb-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-100 text-indigo-600">
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-slate-900">Student Profile</h3>
              </div>
              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                {renderInput("age", "number", "15", "80", "1", "e.g. 21")}
                {renderSelect("gender", getOptions("gender"))}
                {renderSelect("relationship_status", getOptions("relationship_status"))}
                {renderSelect("living_arrangement", getOptions("living_arrangement"))}
                {renderSelect("health_issues", getOptions("health_issues"))}
                {renderSelect("physical_disability", getOptions("physical_disability"))}
              </div>
            </section>

            {/* ACADEMIC SECTION */}
            <section className="rounded-2xl border border-slate-100 bg-white p-6 shadow-sm ring-1 ring-slate-900/5">
              <div className="mb-5 flex items-center gap-2 border-b border-slate-100 pb-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-purple-100 text-purple-600">
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" />
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-slate-900">Academic History</h3>
              </div>
              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                {renderInput("admission_year", "number", "1990", "2035", "1", "e.g. 2022")}
                {renderInput("hsc_year", "number", "1990", "2035", "1", "e.g. 2020")}
                {renderSelect("scholarship", getOptions("scholarship"))}
                {renderSelect("english_proficiency", getOptions("english_proficiency"))}
              </div>
            </section>

            {/* BEHAVIOR SECTION */}
            <section className="rounded-2xl border border-slate-100 bg-white p-6 shadow-sm ring-1 ring-slate-900/5">
              <div className="mb-5 flex items-center gap-2 border-b border-slate-100 pb-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-pink-100 text-pink-600">
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-slate-900">Study & Habits</h3>
              </div>
              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                {renderInput("study_hours", "number", "0", "24", "0.5", "e.g. 5")}
                {renderInput("study_sessions", "number", "0", "30", "1", "e.g. 2")}
                {renderInput("social_media_hours", "number", "0", "24", "0.5", "e.g. 3")}
                {renderInput("skill_development_hours", "number", "0", "24", "0.5", "e.g. 2")}
              </div>
            </section>

            {/* ACTION BUTTONS */}
            <div className="flex flex-col-reverse gap-4 pt-4 sm:flex-row sm:justify-end">
              <button
                type="button"
                onClick={handleReset}
                disabled={predicting}
                className="w-full rounded-xl border border-slate-200 bg-white px-8 py-4 font-bold text-slate-600 transition-all hover:bg-slate-50 hover:text-slate-900 sm:w-auto"
              >
                Clear Form
              </button>
              
              <button
                type="submit"
                disabled={predicting || loadingOptions}
                className="group relative flex w-full items-center justify-center gap-2 overflow-hidden rounded-xl bg-indigo-600 px-8 py-4 font-bold text-white shadow-lg shadow-indigo-500/30 transition-all hover:-translate-y-0.5 hover:shadow-indigo-500/50 focus:ring-4 focus:ring-indigo-500/30 disabled:cursor-not-allowed disabled:opacity-70 sm:w-auto"
              >
                <div className="absolute inset-0 flex h-full w-full justify-center [transform:skew(-12deg)_translateX(-150%)] group-hover:duration-1000 group-hover:[transform:skew(-12deg)_translateX(150%)]">
                  <div className="relative h-full w-8 bg-white/20" />
                </div>
                {predicting ? (
                  <>
                    <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    Generate Prediction
                    <svg className="h-5 w-5 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* ==========================================================
          LAVISH RESULT CARD
      =========================================================== */}
      {prediction !== null && (
        <div className="relative overflow-hidden rounded-3xl bg-slate-900 p-1 shadow-2xl shadow-indigo-500/20 animate-in zoom-in-95 duration-500">
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-500 opacity-20 blur-xl"></div>
          
          <div className="relative flex flex-col items-center justify-center rounded-[22px] bg-slate-900 p-12 text-center border border-slate-800/50">
            <span className="mb-4 inline-flex items-center gap-1.5 rounded-full bg-indigo-500/10 px-3 py-1 text-sm font-semibold text-indigo-400 ring-1 ring-indigo-500/20">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-indigo-400 opacity-75"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-indigo-500"></span>
              </span>
              Analysis Complete
            </span>
            
            <p className="text-lg font-medium text-slate-400">Predicted Academic CGPA</p>
            
            <div className="mt-4 flex items-baseline justify-center gap-2">
              <span className="bg-gradient-to-br from-white to-slate-400 bg-clip-text text-8xl font-black tracking-tighter text-transparent">
                {prediction}
              </span>
              <span className="text-2xl font-bold text-slate-600">/ 4.0</span>
            </div>
            
            <p className="mt-6 max-w-md text-sm text-slate-500">
              This estimate is generated using a trained model based on the academic and behavioral parameters provided.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default PremiumPredictionForm;