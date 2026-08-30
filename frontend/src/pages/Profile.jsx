import {useEffect, useState } from "react";

import {
  User,
  MapPin,
  Phone,
  Mail,
  Sprout,
  Ruler,
  Droplets,
  Save,
  CheckCircle2,
  Pencil,
  ShieldCheck,
} from "lucide-react";

function Profile() {

  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [phone, setPhone] =
    useState("");

  const [state, setState] =
    useState("");

  const [district, setDistrict] =
    useState("");

  const [farmSize, setFarmSize] =
    useState("");

  const [mainCrop, setMainCrop] =
    useState("");

  const [irrigation, setIrrigation] =
    useState("");

  const [editing, setEditing] =
    useState(true);

  const [saved, setSaved] =
    useState(false);


  /* =====================================================
     SAVE PROFILE
  ===================================================== */

  const handleSave = (event) => {

    event.preventDefault();

    const profile = {
      name,
      email,
      phone,
      state,
      district,
      farmSize,
      mainCrop,
      irrigation,
    };

    localStorage.setItem(
      "agrisphere_profile",
      JSON.stringify(profile)
    );

    setSaved(true);

    setEditing(false);

    setTimeout(() => {
      setSaved(false);
    }, 2500);

  };


  /* =====================================================
     LOAD SAVED PROFILE
  ===================================================== */

  useEffect(() => {

    try {

      const savedProfile =
        localStorage.getItem(
          "agrisphere_profile"
        );

      if (!savedProfile) {
        return;
      }

      const profile =
        JSON.parse(savedProfile);

      setName(profile.name || "");
      setEmail(profile.email || "");
      setPhone(profile.phone || "");
      setState(profile.state || "");
      setDistrict(profile.district || "");
      setFarmSize(profile.farmSize || "");
      setMainCrop(profile.mainCrop || "");
      setIrrigation(profile.irrigation || "");

      setEditing(false);

    } catch (error) {

      console.error(
        "Unable to load profile:",
        error
      );

    }

  });


  return (

    <div className="profile-page agent-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <section className="agent-page-header">

        <div>

          <div className="agent-eyebrow">

            <User size={14} />

            FARMER PROFILE

          </div>


          <h1>
            Your farming profile
          </h1>


          <p>
            Keep your basic farm information
            updated so AgriSphere can provide
            more relevant recommendations.
          </p>

        </div>


        <div className="agent-header-icon">

          <User size={31} />

        </div>

      </section>


      {/* =================================================
          PROFILE CONTENT
      ================================================= */}

      <div className="profile-layout">


        {/* =================================================
            PROFILE SUMMARY
        ================================================= */}

        <section className="profile-summary-card">

          <div className="profile-avatar">

            {name
              ? name
                  .charAt(0)
                  .toUpperCase()
              : "F"}

          </div>


          <h2>
            {name || "Farmer"}
          </h2>


          <p>
            {district && state
              ? `${district}, ${state}`
              : "Add your farm location"}
          </p>


          <div className="profile-status">

            <ShieldCheck size={14} />

            AgriSphere profile

          </div>


          <div className="profile-summary-divider" />


          <div className="profile-summary-item">

            <Sprout size={15} />

            <div>

              <span>
                Main crop
              </span>

              <strong>
                {mainCrop || "Not added"}
              </strong>

            </div>

          </div>


          <div className="profile-summary-item">

            <Ruler size={15} />

            <div>

              <span>
                Farm size
              </span>

              <strong>
                {farmSize
                  ? `${farmSize} acres`
                  : "Not added"}
              </strong>

            </div>

          </div>


          <div className="profile-summary-item">

            <Droplets size={15} />

            <div>

              <span>
                Irrigation
              </span>

              <strong>
                {irrigation || "Not added"}
              </strong>

            </div>

          </div>

        </section>


        {/* =================================================
            PROFILE FORM
        ================================================= */}

        <section className="profile-form-card">


          <div className="profile-form-header">

            <div>

              <span>
                PERSONAL INFORMATION
              </span>

              <h2>
                Profile details
              </h2>

            </div>


            {!editing && (

              <button
                type="button"
                className="profile-edit-button"
                onClick={() =>
                  setEditing(true)
                }
              >

                <Pencil size={14} />

                Edit

              </button>

            )}

          </div>


          <form
            onSubmit={handleSave}
            className="profile-form"
          >


            {/* NAME */}

            <div className="agent-field">

              <label>

                <User size={14} />

                Full name

              </label>


              <input
                type="text"
                value={name}
                disabled={!editing}
                onChange={(event) =>
                  setName(
                    event.target.value
                  )
                }
                placeholder="Your name"
              />

            </div>


            {/* EMAIL */}

            <div className="agent-field">

              <label>

                <Mail size={14} />

                Email

              </label>


              <input
                type="email"
                value={email}
                disabled={!editing}
                onChange={(event) =>
                  setEmail(
                    event.target.value
                  )
                }
                placeholder="your@email.com"
              />

            </div>


            {/* PHONE */}

            <div className="agent-field">

              <label>

                <Phone size={14} />

                Phone

              </label>


              <input
                type="tel"
                value={phone}
                disabled={!editing}
                onChange={(event) =>
                  setPhone(
                    event.target.value
                  )
                }
                placeholder="+91 XXXXX XXXXX"
              />

            </div>


            {/* STATE */}

            <div className="agent-field">

              <label>

                <MapPin size={14} />

                State

              </label>


              <input
                type="text"
                value={state}
                disabled={!editing}
                onChange={(event) =>
                  setState(
                    event.target.value
                  )
                }
                placeholder="e.g. Maharashtra"
              />

            </div>


            {/* DISTRICT */}

            <div className="agent-field">

              <label>

                <MapPin size={14} />

                District

              </label>


              <input
                type="text"
                value={district}
                disabled={!editing}
                onChange={(event) =>
                  setDistrict(
                    event.target.value
                  )
                }
                placeholder="e.g. Thane"
              />

            </div>


            {/* FARM SIZE */}

            <div className="agent-field">

              <label>

                <Ruler size={14} />

                Farm size

              </label>


              <input
                type="number"
                min="0"
                step="0.1"
                value={farmSize}
                disabled={!editing}
                onChange={(event) =>
                  setFarmSize(
                    event.target.value
                  )
                }
                placeholder="Farm size in acres"
              />

            </div>


            {/* MAIN CROP */}

            <div className="agent-field">

              <label>

                <Sprout size={14} />

                Main crop

              </label>


              <input
                type="text"
                value={mainCrop}
                disabled={!editing}
                onChange={(event) =>
                  setMainCrop(
                    event.target.value
                  )
                }
                placeholder="e.g. Wheat"
              />

            </div>


            {/* IRRIGATION */}

            <div className="agent-field">

              <label>

                <Droplets size={14} />

                Irrigation

              </label>


              <select
                value={irrigation}
                disabled={!editing}
                onChange={(event) =>
                  setIrrigation(
                    event.target.value
                  )
                }
              >

                <option value="">
                  Select irrigation
                </option>

                <option value="Rainfed">
                  Rainfed
                </option>

                <option value="Drip">
                  Drip
                </option>

                <option value="Sprinkler">
                  Sprinkler
                </option>

                <option value="Canal">
                  Canal
                </option>

                <option value="Borewell">
                  Borewell
                </option>

                <option value="Other">
                  Other
                </option>

              </select>

            </div>


            {/* SAVE */}

            {editing && (

              <div className="profile-save-row">

                <button
                  type="submit"
                  className="agent-primary-button"
                >

                  <Save size={16} />

                  Save profile

                </button>


                {saved && (

                  <span className="profile-saved">

                    <CheckCircle2 size={14} />

                    Profile saved

                  </span>

                )}

              </div>

            )}

          </form>

        </section>

      </div>

    </div>

  );
}

export default Profile;