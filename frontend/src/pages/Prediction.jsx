import { useEffect, useState, useRef } from "react";

import {
  BrainCircuit,
  Sparkles,
  ShieldCheck,
  GraduationCap,
  BookOpen,
  Users,
  Loader2,
  CheckCircle2,
  AlertCircle,
  ChevronDown,
} from "lucide-react";

import api from "../api/api";


// ============================================================
// DEFAULT FORM
// ============================================================

const DEFAULT_FORM = {
  age: 21,

  gender: "",

  relationship_status: "",

  living_arrangement: "",

  health_issues: "",

  physical_disability: "",

  admission_year: 2022,

  hsc_year: 2020,

  scholarship: "",

  english_proficiency: "",

  study_hours: 5,

  study_sessions: 2,

  social_media_hours: 3,

  skill_development_hours: 2,

  current_semester: 6,

  attendance: 88,

  completed_credits: 78,
};


// ============================================================
// HELPER
// ============================================================

const getUniqueOptions = (optionsList = []) => {

  const uniqueValues = [];

  const seen = new Set();

  for (const value of optionsList) {

    const cleanedValue =
      String(value ?? "").trim();

    if (!cleanedValue) {
      continue;
    }

    const normalized =
      cleanedValue.toLowerCase();

    if (seen.has(normalized)) {
      continue;
    }

    seen.add(normalized);

    uniqueValues.push(
      cleanedValue
    );
  }

  return uniqueValues;
};


// ============================================================
// REUSABLE SELECT FIELD
// ============================================================

const SelectField = ({
  name,
  label,
  value,
  onChange,
  optionsList,
  disabled,
}) => {

  const uniqueOptions =
    getUniqueOptions(
      optionsList
    );

  return (

    <div className="space-y-1.5 group">

      <label
        className="
          block
          text-sm
          font-bold
          tracking-wide
          text-slate-700
        "
      >
        {label}
      </label>


      <div className="relative">

        <select
          name={name}
          value={value}
          onChange={onChange}
          disabled={disabled}
          className="
            w-full
            appearance-none
            rounded-xl
            border
            border-slate-200
            bg-slate-50/50
            px-4
            py-3.5
            pr-12
            text-sm
            text-slate-800
            outline-none
            transition-all
            duration-300
            focus:border-indigo-500
            focus:bg-white
            focus:ring-4
            focus:ring-indigo-500/20
            disabled:cursor-not-allowed
            disabled:opacity-60
            group-hover:border-indigo-300
          "
        >

          <option
            value=""
            disabled
          >
            Select {label}
          </option>


          {uniqueOptions.map(
            (option) => (

              <option
                key={`${name}-${option}`}
                value={option}
              >
                {option}
              </option>

            )
          )}

        </select>


        <div
          className="
            pointer-events-none
            absolute
            inset-y-0
            right-4
            flex
            items-center
            text-slate-400
            transition-colors
            group-hover:text-indigo-500
          "
        >

          <ChevronDown
            size={18}
            strokeWidth={2.5}
          />

        </div>

      </div>

    </div>
  );
};


// ============================================================
// REUSABLE NUMBER FIELD
// ============================================================

const NumberField = ({
  name,
  label,
  value,
  onChange,
  min,
  max,
  step = 1,
  disabled,
}) => (

  <div className="space-y-1.5 group">

    <label
      className="
        flex
        items-center
        justify-between
        text-sm
        font-bold
        tracking-wide
        text-slate-700
      "
    >

      <span>
        {label}
      </span>

      <span
        className="
          hidden
          text-[10px]
          font-semibold
          uppercase
          tracking-wider
          text-slate-400
          transition-opacity
          duration-300
          lg:block
          lg:opacity-0
          lg:group-hover:opacity-100
        "
      >
        {min} – {max}
      </span>

    </label>


    <input
      type="number"
      name={name}
      value={value}
      onChange={onChange}
      min={min}
      max={max}
      step={step}
      disabled={disabled}
      className="
        w-full
        rounded-xl
        border
        border-slate-200
        bg-slate-50/50
        px-4
        py-3.5
        text-sm
        text-slate-800
        outline-none
        transition-all
        duration-300
        focus:border-indigo-500
        focus:bg-white
        focus:ring-4
        focus:ring-indigo-500/20
        disabled:cursor-not-allowed
        disabled:opacity-60
        group-hover:border-indigo-300
      "
    />

  </div>
);


// ============================================================
// PAGE
// ============================================================

function Prediction() {

  // ==========================================================
  // STATE
  // ==========================================================

  const [
    options,
    setOptions,
  ] = useState({
    categorical: {},
    numerical_ranges: {},
  });


  const [
    formData,
    setFormData,
  ] = useState(
    DEFAULT_FORM
  );


  const [
    optionsLoading,
    setOptionsLoading,
  ] = useState(true);


  const [
    loading,
    setLoading,
  ] = useState(false);


  const [
    prediction,
    setPrediction,
  ] = useState(null);


  const [
    error,
    setError,
  ] = useState("");


  const resultRef =
    useRef(null);


  // ==========================================================
  // LOAD OPTIONS
  // ==========================================================

  useEffect(() => {

    loadOptions();

  }, []);


  // ==========================================================
  // AUTO SCROLL TO RESULT
  // ==========================================================

  useEffect(() => {

    if (
      prediction &&
      resultRef.current
    ) {

      const timer =
        setTimeout(() => {

          resultRef.current.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });

        }, 100);

      return () => {
        clearTimeout(timer);
      };
    }

  }, [prediction]);


  // ==========================================================
  // LOAD OPTIONS
  // ==========================================================

  const loadOptions = async () => {

    try {

      setOptionsLoading(true);

      setError("");


      const response =
        await api.get(
          "/api/predict/options"
        );


      const data =
        response.data || {};


      const categorical =
        data.categorical || {};


      const numericalRanges =
        data.numerical_ranges || {};


      setOptions({
        categorical,
        numerical_ranges:
          numericalRanges,
      });


      // ------------------------------------------------------
      // First valid values
      // ------------------------------------------------------

      setFormData((previous) => ({

        ...previous,

        gender:
          previous.gender ||
          getUniqueOptions(
            categorical.Gender
          )[0] ||
          "",


        relationship_status:
          previous.relationship_status ||
          getUniqueOptions(
            categorical[
              "What is your relationship status?"
            ]
          )[0] ||
          "",


        living_arrangement:
          previous.living_arrangement ||
          getUniqueOptions(
            categorical[
              "With whom you are living with?"
            ]
          )[0] ||
          "",


        health_issues:
          previous.health_issues ||
          getUniqueOptions(
            categorical[
              "Do you have any health issues?"
            ]
          )[0] ||
          "",


        physical_disability:
          previous.physical_disability ||
          getUniqueOptions(
            categorical[
              "Do you have any physical disabilities?"
            ]
          )[0] ||
          "",


        scholarship:
          previous.scholarship ||
          getUniqueOptions(
            categorical[
              "Do you have meritorious scholarship ?"
            ]
          )[0] ||
          "",


        english_proficiency:
          previous.english_proficiency ||
          getUniqueOptions(
            categorical[
              "Status of your English language proficiency"
            ]
          )[0] ||
          "",
      }));


    } catch (err) {

      console.error(
        "Prediction Options Error:",
        err
      );


      setError(
        err.response?.data?.detail ||
        "Unable to load prediction options."
      );


    } finally {

      setOptionsLoading(false);

    }
  };


  // ==========================================================
  // HANDLE CHANGE
  // ==========================================================

  const handleChange = (
    event
  ) => {

    const {
      name,
      value,
    } = event.target;


    const numericFields = [

      "age",

      "admission_year",

      "hsc_year",

      "study_hours",

      "study_sessions",

      "social_media_hours",

      "skill_development_hours",

      "current_semester",

      "attendance",

      "completed_credits",

    ];


    setFormData((previous) => ({

      ...previous,

      [name]: numericFields.includes(
        name
      )
        ? Number(value)
        : value,

    }));


    setPrediction(null);

    setError("");
  };


  // ==========================================================
  // RESET
  // ==========================================================

  const handleReset = () => {

    const categorical =
      options.categorical || {};


    const firstOption = (
      key
    ) => {

      return (
        getUniqueOptions(
          categorical[key]
        )[0] ||
        ""
      );

    };


    setFormData({

      ...DEFAULT_FORM,


      gender:
        firstOption(
          "Gender"
        ),


      relationship_status:
        firstOption(
          "What is your relationship status?"
        ),


      living_arrangement:
        firstOption(
          "With whom you are living with?"
        ),


      health_issues:
        firstOption(
          "Do you have any health issues?"
        ),


      physical_disability:
        firstOption(
          "Do you have any physical disabilities?"
        ),


      scholarship:
        firstOption(
          "Do you have meritorious scholarship ?"
        ),


      english_proficiency:
        firstOption(
          "Status of your English language proficiency"
        ),

    });


    setPrediction(null);

    setError("");


    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };


  // ==========================================================
  // FORM VALIDATION
  // ==========================================================

  const validateForm = () => {

    const requiredCategorical = [

      [
        "gender",
        "Gender",
      ],

      [
        "relationship_status",
        "Relationship Status",
      ],

      [
        "living_arrangement",
        "Living Arrangement",
      ],

      [
        "health_issues",
        "Health Issues",
      ],

      [
        "physical_disability",
        "Physical Disability",
      ],

      [
        "scholarship",
        "Scholarship",
      ],

      [
        "english_proficiency",
        "English Proficiency",
      ],

    ];


    for (
      const [
        field,
        label,
      ]
      of requiredCategorical
    ) {

      if (
        !String(
          formData[field] ?? ""
        ).trim()
      ) {

        setError(
          `Please select ${label}.`
        );

        return false;
      }
    }


    if (
      formData.current_semester <
      1 ||
      formData.current_semester >
      12
    ) {

      setError(
        "Current Semester must be between 1 and 12."
      );

      return false;
    }


    if (
      formData.attendance <
      0 ||
      formData.attendance >
      100
    ) {

      setError(
        "Attendance must be between 0 and 100."
      );

      return false;
    }


    if (
      formData.completed_credits <
      0 ||
      formData.completed_credits >
      145
    ) {

      setError(
        "Completed Credits must be between 0 and 145."
      );

      return false;
    }


    return true;
  };


  // ==========================================================
  // SUBMIT
  // ==========================================================

  const handlePrediction = async (
    event
  ) => {

    event.preventDefault();


    setError("");

    setPrediction(null);


    if (
      !validateForm()
    ) {

      return;
    }


    try {

      setLoading(true);


      const response =
        await api.post(
          "/api/predict/",
          formData
        );


      setPrediction(
        response.data || {}
      );


    } catch (err) {

      console.error(
        "Prediction Error:",
        err
      );


      setError(
        err.response?.data?.detail ||
        "Prediction failed. Please check the backend."
      );


    } finally {

      setLoading(false);

    }
  };


  // ==========================================================
  // LOADING SCREEN
  // ==========================================================

  if (
    optionsLoading
  ) {

    return (

      <div
        className="
          flex
          min-h-[70vh]
          items-center
          justify-center
        "
      >

        <div className="text-center">

          <div
            className="
              mx-auto
              flex
              h-20
              w-20
              items-center
              justify-center
              rounded-3xl
              bg-indigo-50
              shadow-inner
              ring-1
              ring-indigo-100
            "
          >

            <Loader2
              size={36}
              className="
                animate-spin
                text-indigo-600
              "
            />

          </div>


          <h2
            className="
              mt-6
              text-2xl
              font-extrabold
              tracking-tight
              text-slate-900
            "
          >
            Initializing Prediction Engine
          </h2>


          <p
            className="
              mt-2
              text-slate-500
            "
          >
            Loading student options and model configuration...
          </p>

        </div>

      </div>
    );
  }


  // ==========================================================
  // MAIN PAGE
  // ==========================================================

  return (

    <div
      className="
        mx-auto
        w-full
        max-w-5xl
        space-y-8
        animate-in
        fade-in
        duration-500
      "
    >

      {/* ======================================================
          HEADER
      ====================================================== */}

      <div
        className="
          flex
          items-center
          gap-4
        "
      >

        <div
          className="
            flex
            h-14
            w-14
            items-center
            justify-center
            rounded-2xl
            bg-indigo-600
            text-white
            shadow-lg
            shadow-indigo-600/20
          "
        >

          <BrainCircuit
            size={28}
            strokeWidth={2}
          />

        </div>


        <div>

          <h1
            className="
              text-4xl
              font-extrabold
              tracking-tight
              text-slate-900
            "
          >
            CGPA Prediction
          </h1>


          <p
            className="
              mt-1
              font-medium
              text-slate-500
            "
          >
            Estimate student academic performance using
            academic, demographic and study information.
          </p>

        </div>

      </div>


      {/* ======================================================
          INFO CARDS
      ====================================================== */}

      <div
        className="
          grid
          grid-cols-1
          gap-5
          md:grid-cols-3
        "
      >

        {[
          {
            title:
              "Data-Driven Prediction",

            desc:
              "Academic performance estimate",

            icon:
              BrainCircuit,

            color:
              "text-blue-600",

            bg:
              "bg-blue-50",
          },

          {
            title:
              "Privacy First",

            desc:
              "Local prediction service",

            icon:
              ShieldCheck,

            color:
              "text-emerald-600",

            bg:
              "bg-emerald-50",
          },

          {
            title:
              "Context Aware",

            desc:
              "Attendance and credits included",

            icon:
              GraduationCap,

            color:
              "text-purple-600",

            bg:
              "bg-purple-50",
          },

        ].map(
          (
            card,
            index
          ) => {

            const Icon =
              card.icon;

            return (

              <div
                key={index}
                className="
                  group
                  flex
                  items-center
                  gap-4
                  rounded-2xl
                  border
                  border-slate-200
                  bg-white
                  p-5
                  shadow-sm
                  transition-all
                  hover:-translate-y-1
                  hover:shadow-md
                "
              >

                <div
                  className={`
                    flex
                    h-12
                    w-12
                    shrink-0
                    items-center
                    justify-center
                    rounded-xl
                    transition-transform
                    group-hover:scale-105
                    ${card.bg}
                  `}
                >

                  <Icon
                    size={22}
                    className={
                      card.color
                    }
                  />

                </div>


                <div>

                  <h3
                    className="
                      font-bold
                      text-slate-800
                    "
                  >
                    {card.title}
                  </h3>


                  <p
                    className="
                      text-xs
                      font-medium
                      text-slate-500
                    "
                  >
                    {card.desc}
                  </p>

                </div>

              </div>
            );
          }
        )}

      </div>


      {/* ======================================================
          FORM
      ====================================================== */}

      <form
        onSubmit={
          handlePrediction
        }
        className="
          space-y-8
        "
      >

        {/* ====================================================
            SECTION 1
        ==================================================== */}

        <div
          className="
            overflow-hidden
            rounded-3xl
            border
            border-slate-200
            bg-white
            shadow-sm
            ring-1
            ring-slate-900/5
          "
        >

          <div
            className="
              border-b
              border-slate-100
              bg-slate-50/50
              px-8
              py-6
            "
          >

            <div
              className="
                flex
                items-center
                gap-3
              "
            >

              <Users
                size={24}
                className="text-indigo-600"
              />


              <div>

                <h2
                  className="
                    text-xl
                    font-bold
                    text-slate-900
                  "
                >
                  Student Profile
                </h2>


                <p
                  className="
                    text-sm
                    text-slate-500
                  "
                >
                  Demographic and personal context
                </p>

              </div>

            </div>

          </div>


          <div
            className="
              grid
              grid-cols-1
              gap-6
              p-8
              md:grid-cols-2
              lg:grid-cols-3
            "
          >

            <NumberField
              name="age"
              label="Age"
              value={
                formData.age
              }
              onChange={
                handleChange
              }
              min={15}
              max={80}
              disabled={
                loading
              }
            />


            <SelectField
              name="gender"
              label="Gender"
              value={
                formData.gender
              }
              onChange={
                handleChange
              }
              optionsList={
                options.categorical?.Gender
              }
              disabled={
                loading
              }
            />


            <SelectField
              name="relationship_status"
              label="Relationship Status"
              value={
                formData.relationship_status
              }
              onChange={
                handleChange
              }
              optionsList={
                options.categorical?.[
                  "What is your relationship status?"
                ]
              }
              disabled={
                loading
              }
            />


            <SelectField
              name="living_arrangement"
              label="Living Arrangement"
              value={
                formData.living_arrangement
              }
              onChange={
                handleChange
              }
              optionsList={
                options.categorical?.[
                  "With whom you are living with?"
                ]
              }
              disabled={
                loading
              }
            />


            <SelectField
              name="health_issues"
              label="Health Issues"
              value={
                formData.health_issues
              }
              onChange={
                handleChange
              }
              optionsList={
                options.categorical?.[
                  "Do you have any health issues?"
                ]
              }
              disabled={
                loading
              }
            />


            <SelectField
              name="physical_disability"
              label="Physical Disability"
              value={
                formData.physical_disability
              }
              onChange={
                handleChange
              }
              optionsList={
                options.categorical?.[
                  "Do you have any physical disabilities?"
                ]
              }
              disabled={
                loading
              }
            />

          </div>

        </div>


        {/* ====================================================
            SECTION 2
        ==================================================== */}

        <div
          className="
            overflow-hidden
            rounded-3xl
            border
            border-slate-200
            bg-white
            shadow-sm
            ring-1
            ring-slate-900/5
          "
        >

          <div
            className="
              border-b
              border-slate-100
              bg-slate-50/50
              px-8
              py-6
            "
          >

            <div
              className="
                flex
                items-center
                gap-3
              "
            >

              <GraduationCap
                size={24}
                className="text-purple-600"
              />


              <div>

                <h2
                  className="
                    text-xl
                    font-bold
                    text-slate-900
                  "
                >
                  Academic Context
                </h2>


                <p
                  className="
                    text-sm
                    text-slate-500
                  "
                >
                  University metrics and language proficiency
                </p>

              </div>

            </div>

          </div>


          <div
            className="
              grid
              grid-cols-1
              gap-6
              p-8
              md:grid-cols-2
              lg:grid-cols-3
            "
          >

            <NumberField
              name="admission_year"
              label="Admission Year"
              value={
                formData.admission_year
              }
              onChange={
                handleChange
              }
              min={1990}
              max={2035}
              disabled={
                loading
              }
            />


            <NumberField
              name="hsc_year"
              label="H.S.C Passing Year"
              value={
                formData.hsc_year
              }
              onChange={
                handleChange
              }
              min={1990}
              max={2035}
              disabled={
                loading
              }
            />


            <SelectField
              name="scholarship"
              label="Scholarship / Waiver"
              value={
                formData.scholarship
              }
              onChange={
                handleChange
              }
              optionsList={
                options.categorical?.[
                  "Do you have meritorious scholarship ?"
                ]
              }
              disabled={
                loading
              }
            />


            <SelectField
              name="english_proficiency"
              label="English Proficiency"
              value={
                formData.english_proficiency
              }
              onChange={
                handleChange
              }
              optionsList={
                options.categorical?.[
                  "Status of your English language proficiency"
                ]
              }
              disabled={
                loading
              }
            />


            <NumberField
              name="current_semester"
              label="Current Semester"
              value={
                formData.current_semester
              }
              onChange={
                handleChange
              }
              min={1}
              max={12}
              disabled={
                loading
              }
            />


            <NumberField
              name="completed_credits"
              label="Completed Credits"
              value={
                formData.completed_credits
              }
              onChange={
                handleChange
              }
              min={0}
              max={145}
              disabled={
                loading
              }
            />

          </div>

        </div>


        {/* ====================================================
            SECTION 3
        ==================================================== */}

        <div
          className="
            overflow-hidden
            rounded-3xl
            border
            border-slate-200
            bg-white
            shadow-sm
            ring-1
            ring-slate-900/5
          "
        >

          <div
            className="
              border-b
              border-slate-100
              bg-slate-50/50
              px-8
              py-6
            "
          >

            <div
              className="
                flex
                items-center
                gap-3
              "
            >

              <BookOpen
                size={24}
                className="text-amber-600"
              />


              <div>

                <h2
                  className="
                    text-xl
                    font-bold
                    text-slate-900
                  "
                >
                  Study & Habits
                </h2>


                <p
                  className="
                    text-sm
                    text-slate-500
                  "
                >
                  Daily routines and academic engagement
                </p>

              </div>

            </div>

          </div>


          <div
            className="
              grid
              grid-cols-1
              gap-6
              p-8
              md:grid-cols-2
              lg:grid-cols-3
            "
          >

            <NumberField
              name="study_hours"
              label="Daily Study Hours"
              value={
                formData.study_hours
              }
              onChange={
                handleChange
              }
              min={0}
              max={24}
              step={0.5}
              disabled={
                loading
              }
            />


            <NumberField
              name="study_sessions"
              label="Sessions per Day"
              value={
                formData.study_sessions
              }
              onChange={
                handleChange
              }
              min={0}
              max={30}
              disabled={
                loading
              }
            />


            <NumberField
              name="social_media_hours"
              label="Social Media Hours"
              value={
                formData.social_media_hours
              }
              onChange={
                handleChange
              }
              min={0}
              max={24}
              step={0.5}
              disabled={
                loading
              }
            />


            <NumberField
              name="skill_development_hours"
              label="Skill Development Hours"
              value={
                formData.skill_development_hours
              }
              onChange={
                handleChange
              }
              min={0}
              max={24}
              step={0.5}
              disabled={
                loading
              }
            />


            <NumberField
              name="attendance"
              label="Average Attendance (%)"
              value={
                formData.attendance
              }
              onChange={
                handleChange
              }
              min={0}
              max={100}
              step={0.5}
              disabled={
                loading
              }
            />

          </div>

        </div>


        {/* ====================================================
            ERROR
        ==================================================== */}

        {error && (

          <div
            className="
              flex
              items-center
              gap-3
              rounded-2xl
              border
              border-rose-200
              bg-rose-50
              p-5
              text-rose-700
            "
          >

            <AlertCircle
              size={24}
              className="shrink-0"
            />


            <span
              className="
                font-semibold
              "
            >
              {error}
            </span>

          </div>

        )}


        {/* ====================================================
            BUTTONS
        ==================================================== */}

        <div
          className="
            flex
            flex-col-reverse
            gap-4
            pt-4
            sm:flex-row
            sm:justify-end
          "
        >

          <button
            type="button"
            onClick={
              handleReset
            }
            disabled={
              loading
            }
            className="
              rounded-xl
              border
              border-slate-300
              bg-white
              px-8
              py-4
              font-bold
              text-slate-700
              shadow-sm
              transition
              hover:bg-slate-50
              focus:ring-4
              focus:ring-slate-100
              disabled:opacity-50
            "
          >
            Reset Form
          </button>


          <button
            type="submit"
            disabled={
              loading
            }
            className="
              flex
              items-center
              justify-center
              gap-3
              rounded-xl
              bg-indigo-600
              px-10
              py-4
              font-bold
              text-white
              shadow-lg
              shadow-indigo-500/20
              transition-all
              hover:bg-indigo-700
              hover:shadow-indigo-500/30
              active:scale-[0.98]
              disabled:pointer-events-none
              disabled:opacity-70
            "
          >

            {loading ? (

              <>

                <Loader2
                  size={22}
                  className="animate-spin"
                />

                Analyzing Data...

              </>

            ) : (

              <>

                <Sparkles
                  size={22}
                />

                Generate Prediction

              </>

            )}

          </button>

        </div>

      </form>


      {/* ======================================================
          RESULT
      ====================================================== */}

      {prediction && (

        <div
          ref={resultRef}
          className="
            pt-8
          "
        >

          <div
            className="
              overflow-hidden
              rounded-[2rem]
              border
              border-slate-800
              bg-slate-900
              shadow-2xl
              shadow-slate-900/10
            "
          >

            <div
              className="
                flex
                flex-col
                items-center
                justify-center
                px-8
                py-12
                text-center
                md:px-12
                md:py-14
              "
            >

              <div
                className="
                  mb-6
                  flex
                  items-center
                  gap-2
                  rounded-full
                  border
                  border-emerald-500/30
                  bg-emerald-500/10
                  px-4
                  py-2
                  text-sm
                  font-bold
                  text-emerald-400
                "
              >

                <CheckCircle2
                  size={18}
                />

                Prediction Complete

              </div>


              <h3
                className="
                  text-base
                  font-medium
                  tracking-wide
                  text-slate-400
                "
              >
                Predicted Academic CGPA
              </h3>


              <div
                className="
                  mt-4
                  flex
                  items-baseline
                  justify-center
                  gap-3
                "
              >

                <span
                  className="
                    text-7xl
                    font-black
                    tracking-tighter
                    text-white
                    sm:text-8xl
                  "
                >

                  {Number(
                    prediction.prediction?.predicted_cgpa ??
                    prediction.predicted_cgpa ??
                    0
                  ).toFixed(2)}

                </span>


                <span
                  className="
                    text-2xl
                    font-bold
                    text-slate-500
                    sm:text-3xl
                  "
                >
                  / 4.0
                </span>

              </div>


              <p
                className="
                  mt-7
                  max-w-xl
                  text-sm
                  leading-6
                  text-slate-500
                "
              >
                The displayed estimate is generated from the
                selected demographic, academic, study and
                academic-context information.
              </p>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}


export default Prediction;