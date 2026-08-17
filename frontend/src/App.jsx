// // // import { BrowserRouter, Routes, Route } from "react-router-dom";

// // // import MainLayout from "./layouts/MainLayout";
// // // import Prediction from "./pages/Prediction";
// // // import Dashboard from "./pages/Dashboard";

// // // // Temporary pages
// // // // function Prediction() {
// // // //   return <h1 className="text-3xl font-bold">Prediction Page</h1>;
// // // // }

// // // function Analytics() {
// // //   return <h1 className="text-3xl font-bold">Analytics Page</h1>;
// // // }

// // // function Chatbot() {
// // //   return <h1 className="text-3xl font-bold">AI Chatbot Page</h1>;
// // // }

// // // function App() {
// // //   return (
// // //     <BrowserRouter>
// // //       <MainLayout>
// // //         <Routes>
// // //           <Route path="/" element={<Dashboard />} />

// // //           <Route
// // //             path="/prediction"
// // //             element={<Prediction />}
// // //             />

// // //           <Route
// // //             path="/analytics"
// // //             element={<Analytics />}
// // //           />

// // //           <Route
// // //             path="/chatbot"
// // //             element={<Chatbot />}
// // //           />
// // //         </Routes>
// // //       </MainLayout>
// // //     </BrowserRouter>
// // //   );
// // // }

// // // export default App;




// // import { BrowserRouter, Routes, Route } from "react-router-dom";

// // import MainLayout from "./layouts/MainLayout";

// // import Dashboard from "./pages/Dashboard";
// // import Prediction from "./pages/Prediction";
// // import Analytics from "./pages/Analytics";
// // import Chatbot from "./pages/Chatbot";
// // // Temporary Chatbot page
// // // function Chatbot() {
// // //   return (
// // //     <div className="text-3xl font-bold text-slate-800">
// // //       AI Chatbot
// // //     </div>
// // //   );
// // // }

// // function App() {
// //   return (
// //     <BrowserRouter>
// //       <MainLayout>
// //         <Routes>

// //           {/* Dashboard */}
// //           <Route
// //             path="/"
// //             element={<Dashboard />}
// //           />

// //           {/* Prediction */}
// //           <Route
// //             path="/prediction"
// //             element={<Prediction />}
// //           />

// //           {/* Analytics */}
// //           <Route
// //             path="/analytics"
// //             element={<Analytics />}
// //           />

// //           {/* Chatbot */}
// //           <Route
// //             path="/chatbot"
// //             element={<Chatbot />}
// //           />

// //         </Routes>
// //       </MainLayout>
// //     </BrowserRouter>
// //   );
// // }

// // export default App;




// import { BrowserRouter, Routes, Route } from "react-router-dom";

// import MainLayout from "./layouts/MainLayout";

// import Dashboard from "./pages/Dashboard";
// import Prediction from "./pages/Prediction";
// import Analytics from "./pages/Analytics";
// import Chatbot from "./pages/Chatbot";

// function App() {
//   return (
//     <BrowserRouter>
//       <MainLayout>
//         <Routes>

//           {/* Dashboard */}
//           <Route
//             path="/"
//             element={<Dashboard />}
//           />

//           {/* Prediction */}
//           <Route
//             path="/prediction"
//             element={<Prediction />}
//           />

//           {/* Analytics */}
//           <Route
//             path="/analytics"
//             element={<Analytics />}
//           />

//         </Routes>

//         {/* GLOBAL FLOATING AI ASSISTANT */}
//         <Chatbot />

//       </MainLayout>
//     </BrowserRouter>
//   );
// }

// export default App;











import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Prediction from "./pages/Prediction";
// import Analytics from "./pages/Analytics";
import Chatbot from "./pages/Chatbot";


function App() {
  return (
    <BrowserRouter>

      <MainLayout>

        <Routes>

          {/* ==================================================
              OVERVIEW
          ================================================== */}

          <Route
            path="/"
            element={<Dashboard />}
          />


          {/* ==================================================
              ANALYTICS
          ================================================== */}

          


          {/* ==================================================
              PREDICTION
          ================================================== */}

          <Route
            path="/prediction"
            element={<Prediction />}
          />


          {/* ==================================================
              OPTIONAL CHATBOT PAGE
          ================================================== */}

          <Route
            path="/assistant"
            element={<Chatbot />}
          />

        </Routes>


        {/* ====================================================
            GLOBAL FLOATING AI ASSISTANT
        ==================================================== */}

        <Chatbot />

      </MainLayout>

    </BrowserRouter>
  );
}

export default App;