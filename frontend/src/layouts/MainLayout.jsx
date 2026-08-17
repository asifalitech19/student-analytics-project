import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";


function MainLayout({
  children,
}) {

  return (

    <div
      className="
        flex
        min-h-screen
        bg-slate-50
        text-slate-800
      "
    >

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <Sidebar />


      {/* ======================================================
          MAIN APPLICATION AREA
      ====================================================== */}

      <div
        className="
          flex-1
          min-w-0
          flex
          flex-col
        "
      >

        {/* ====================================================
            TOP NAVBAR
        ==================================================== */}

        <Navbar />


        {/* ====================================================
            PAGE CONTENT
        ==================================================== */}

        <main
          className="
            flex-1
            overflow-auto
            px-6
            py-6
            lg:px-8
            lg:py-8
          "
        >

          <div
            className="
              mx-auto
              w-full
              max-w-[1600px]
            "
          >

            {children}

          </div>

        </main>

      </div>

    </div>
  );
}


export default MainLayout;