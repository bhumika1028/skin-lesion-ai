import React from 'react';
import { User, MapPin, Calendar, Palette, Activity, ShieldAlert, Pill, Cpu, Camera } from 'lucide-react';
import { ClinicalFormData } from '../types/triage';
import { BodyMapSelector } from './BodyMapSelector';

interface ClinicalFormProps {
  formData: ClinicalFormData;
  setFormData: React.Dispatch<React.SetStateAction<ClinicalFormData>>;
}

export const ClinicalForm: React.FC<ClinicalFormProps> = ({ formData, setFormData }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else if (name === 'age') {
      setFormData((prev) => ({ ...prev, age: parseFloat(value) || 0 }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleLocationSelect = (locId: string) => {
    setFormData((prev) => ({ ...prev, lesion_location: locId }));
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
      {/* Model & Uncertainty Engine Architecture Selector */}
      <div className="p-4 bg-teal-50/60 rounded-xl border border-teal-200 space-y-3">
        <h4 className="text-xs font-bold text-teal-900 uppercase tracking-wider flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-teal-600" />
          <span>Model Architecture & Uncertainty Engine Selector</span>
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">AI Architecture Engine</label>
            <select
              name="model_architecture"
              value={formData.model_architecture}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 font-medium text-slate-900 bg-white"
            >
              <option value="swin_edl">Proposed Swin Transformer + Dirichlet EDL (Single Pass)</option>
              <option value="monte_carlo">Monte Carlo Dropout (10 Passes Bayesian Uncertainty)</option>
              <option value="mobile_vit">MobileViT Edge Model (Mobile Vision Transformer)</option>
            </select>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1 flex items-center space-x-1">
              <Camera className="w-3.5 h-3.5 text-slate-500" />
              <span>Image Acquisition Mode (Domain Shift Adaptation)</span>
            </label>
            <select
              name="imaging_mode"
              value={formData.imaging_mode}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 font-medium text-slate-900 bg-white"
            >
              <option value="dermoscopic">Dermoscopic Mode (Standard Handheld Dermatoscope)</option>
              <option value="smartphone">Smartphone Photo Mode (SLICE-3D Dataset Noise Adaptation)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Patient History Questionnaire */}
      <div>
        <h3 className="text-base font-semibold text-slate-900 mb-1 flex items-center space-x-2">
          <User className="w-5 h-5 text-teal-600" />
          <span>Step 2: Patient History & Clinical Questionnaire</span>
        </h3>
        <p className="text-xs text-slate-500 mb-4">
          Patient background, lesion evolution, allergies, and ongoing medications used for multimodal fusion.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* Age */}
          <div>
            <label className="block font-medium text-slate-700 mb-1 flex items-center space-x-1">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              <span>Patient Age (Years)</span>
            </label>
            <input
              type="number"
              name="age"
              min="0"
              max="120"
              value={formData.age}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 text-slate-900"
            />
          </div>

          {/* Biological Sex */}
          <div>
            <label className="block font-medium text-slate-700 mb-1">Biological Sex</label>
            <select
              name="sex"
              value={formData.sex}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 text-slate-900 bg-white"
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Unknown">Prefer not to say / Unknown</option>
            </select>
          </div>

          {/* Fitzpatrick Skin Phototype */}
          <div>
            <label className="block font-medium text-slate-700 mb-1 flex items-center space-x-1">
              <Palette className="w-3.5 h-3.5 text-amber-600" />
              <span>Fitzpatrick Skin Phototype (Bias Mitigation)</span>
            </label>
            <select
              name="fitzpatrick_scale"
              value={formData.fitzpatrick_scale}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 text-slate-900 bg-white"
            >
              <option value="Type I (Pale White / Always Burns)">Type I — Pale White (Always burns, never tans)</option>
              <option value="Type II (Fair / Usually Burns)">Type II — Fair White (Usually burns, tans minimally)</option>
              <option value="Type III (Medium / Olive)">Type III — Medium / Olive (Sometimes burns, tans uniformly)</option>
              <option value="Type IV (Moderate Brown / Rarely Burns)">Type IV — Moderate Brown (Rarely burns, tans easily)</option>
              <option value="Type V (Dark Brown / Very Rarely Burns)">Type V — Dark Brown (Very rarely burns, tans very easily)</option>
              <option value="Type VI (Deeply Pigmented / Never Burns)">Type VI — Deeply Pigmented Dark (Never burns)</option>
            </select>
          </div>

          {/* Lesion Location Body Map Selector */}
          <div className="md:col-span-2">
            <BodyMapSelector
              selectedLocation={formData.lesion_location}
              onSelectLocation={handleLocationSelect}
            />
          </div>

          {/* Evolution */}
          <div>
            <label className="block font-medium text-slate-700 mb-1 flex items-center space-x-1">
              <Activity className="w-3.5 h-3.5 text-slate-400" />
              <span>Has the lesion changed recently?</span>
            </label>
            <select
              name="evolution"
              value={formData.evolution}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 text-slate-900 bg-white"
            >
              <option value="static">No - Lesion has remained static</option>
              <option value="changed_recently">Yes - Changed in size, shape, or color</option>
              <option value="uncertain">Uncertain / Not sure</option>
            </select>
          </div>

          {/* Observed Color */}
          <div className="md:col-span-2">
            <label className="block font-medium text-slate-700 mb-1 flex items-center space-x-1">
              <Palette className="w-3.5 h-3.5 text-slate-400" />
              <span>Observed Dominant Appearance / Color</span>
            </label>
            <select
              name="observed_color"
              value={formData.observed_color}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 text-slate-900 bg-white"
            >
              <option value="brown">Brown</option>
              <option value="black">Black / Dark Pigmented</option>
              <option value="red">Red</option>
              <option value="pink">Pink / Flesh-colored</option>
              <option value="blue_purple">Blue / Purple</option>
              <option value="white">White / Depigmented</option>
              <option value="multiple">Multiple Colors</option>
              <option value="not_sure">Not sure</option>
            </select>
          </div>

          {/* Prior Skin Allergies */}
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <label className="flex items-center space-x-2 cursor-pointer font-medium text-slate-800">
              <input
                type="checkbox"
                name="prior_allergies"
                checked={formData.prior_allergies}
                onChange={handleChange}
                className="rounded border-slate-300 text-teal-600 focus:ring-teal-500 w-4 h-4"
              />
              <span className="flex items-center space-x-1">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-600" />
                <span>History of Skin Allergies / Conditions</span>
              </span>
            </label>
            {formData.prior_allergies && (
              <select
                name="allergy_details"
                value={formData.allergy_details}
                onChange={handleChange}
                className="mt-2 w-full px-3 py-1.5 border border-slate-300 rounded-lg text-slate-900 bg-white"
              >
                <option value="">-- Select Skin Allergy / Condition --</option>
                <option value="Contact Dermatitis (Latex, Fragrance, Dyes)">Contact Dermatitis (Latex, Fragrance, Dyes)</option>
                <option value="Nickel / Heavy Metal Allergy">Nickel / Heavy Metal Allergy</option>
                <option value="Atopic Dermatitis / Eczema">Atopic Dermatitis / Eczema</option>
                <option value="Psoriasis">Psoriasis</option>
                <option value="Urticaria (Hives / Allergic Rash)">Urticaria (Hives / Allergic Rash)</option>
                <option value="Sun / UV Hypersensitivity (Photosensitivity)">Sun / UV Hypersensitivity (Photosensitivity)</option>
                <option value="Topical Cosmetic / Skincare Reaction">Topical Cosmetic / Skincare Reaction</option>
                <option value="Insect Bite / Sting Reaction">Insect Bite / Sting Reaction</option>
                <option value="Drug-Induced Exanthem (Medication Rash)">Drug-Induced Exanthem (Medication Rash)</option>
                <option value="Seborrheic Dermatitis">Seborrheic Dermatitis</option>
                <option value="Rosacea">Rosacea</option>
                <option value="Lichen Planus">Lichen Planus</option>
                <option value="Other Skin Allergy / Condition">Other Skin Allergy / Condition</option>
              </select>
            )}
          </div>

          {/* Ongoing Medications */}
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <label className="flex items-center space-x-2 cursor-pointer font-medium text-slate-800">
              <input
                type="checkbox"
                name="ongoing_medications"
                checked={formData.ongoing_medications}
                onChange={handleChange}
                className="rounded border-slate-300 text-teal-600 focus:ring-teal-500 w-4 h-4"
              />
              <span className="flex items-center space-x-1">
                <Pill className="w-3.5 h-3.5 text-indigo-600" />
                <span>Ongoing Medications / Topical Treatments</span>
              </span>
            </label>
            {formData.ongoing_medications && (
              <select
                name="medication_details"
                value={formData.medication_details}
                onChange={handleChange}
                className="mt-2 w-full px-3 py-1.5 border border-slate-300 rounded-lg text-slate-900 bg-white"
              >
                <option value="">-- Select Medication / Topical Treatment --</option>
                <option value="Topical Corticosteroids (Hydrocortisone, Clobetasol, Betamethasone)">Topical Corticosteroids (Hydrocortisone, Clobetasol, Betamethasone)</option>
                <option value="Topical Calcineurin Inhibitors (Tacrolimus, Pimecrolimus)">Topical Calcineurin Inhibitors (Tacrolimus, Pimecrolimus)</option>
                <option value="Topical Retinoids (Tretinoin, Adapalene, Tazarotene)">Topical Retinoids (Tretinoin, Adapalene, Tazarotene)</option>
                <option value="Oral / Topical Antifungals (Ketoconazole, Clotrimazole, Terbinafine)">Oral / Topical Antifungals (Ketoconazole, Clotrimazole, Terbinafine)</option>
                <option value="Topical Antibiotics (Mupirocin, Neomycin, Clindamycin)">Topical Antibiotics (Mupirocin, Neomycin, Clindamycin)</option>
                <option value="Oral Antihistamines (Cetirizine, Loratadine, Diphenhydramine)">Oral Antihistamines (Cetirizine, Loratadine, Diphenhydramine)</option>
                <option value="Systemic Immunosuppressants (Methotrexate, Cyclosporine)">Systemic Immunosuppressants (Methotrexate, Cyclosporine)</option>
                <option value="Biologics (Dupilumab, Secukinumab, Ustekinumab)">Biologics (Dupilumab, Secukinumab, Ustekinumab)</option>
                <option value="Oral Retinoids (Isotretinoin / Accutane)">Oral Retinoids (Isotretinoin / Accutane)</option>
                <option value="Medicated Shampoos / Tar Preps / Salicylic Acid">Medicated Shampoos / Tar Preps / Salicylic Acid</option>
                <option value="Phototherapy / PUVA Therapy">Phototherapy / PUVA Therapy</option>
                <option value="Other Skin Medication / Topical Treatment">Other Skin Medication / Topical Treatment</option>
              </select>
            )}
          </div>

          {/* Symptoms */}
          <div className="md:col-span-2 pt-2 border-t border-slate-100">
            <span className="block font-medium text-slate-700 mb-2">Present Symptoms:</span>
            <div className="flex flex-wrap gap-4 text-slate-700">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="itching"
                  checked={formData.itching}
                  onChange={handleChange}
                  className="rounded border-slate-300 text-teal-600 focus:ring-teal-500 w-4 h-4"
                />
                <span>Itching</span>
              </label>
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="bleeding"
                  checked={formData.bleeding}
                  onChange={handleChange}
                  className="rounded border-slate-300 text-teal-600 focus:ring-teal-500 w-4 h-4"
                />
                <span>Bleeding / Oozing</span>
              </label>
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="pain"
                  checked={formData.pain}
                  onChange={handleChange}
                  className="rounded border-slate-300 text-teal-600 focus:ring-teal-500 w-4 h-4"
                />
                <span>Pain / Tenderness</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
