type FormInputProps = {
  label: string;
  register: any;
  error?: string;
  placeholder: string;
  type?: string;
};

const FormInput: React.FC<FormInputProps> = ({
  label,
  register,
  error,
  type = "text",
  placeholder,
}) => {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      <input
        {...register}
        type={type}
        placeholder={placeholder}
        className={`w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 ${
          error ? "border-red-500" : "border-gray-300"
        }`}
      />
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
};

export default FormInput;
