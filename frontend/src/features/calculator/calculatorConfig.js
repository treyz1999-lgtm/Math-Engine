export const calculatorConfigs = {
  arithmetic: {
    binary: {
      endpoint: "/arithmetic/binary",
      operations: ["add", "subtract", "multiply", "divide", "mod", "root"],
      fields: [
        { name: "value1", label: "Value 1", type: "number" },
        { name: "value2", label: "Value 2", type: "number" },
      ],
    },
    power: {
      endpoint: "/arithmetic/power",
      operations: ["power"],
      fields: [
        { name: "base", label: "Base", type: "number" },
        { name: "exponent", label: "Exponent", type: "number" },
      ],
    },
    other: {
      endpoint: "/arithmetic/other",
      operations: ["abs", "factorial"],
      fields: [{ name: "value1", label: "Value", type: "number" }],
    },
  },
  trig: {
    basic: {
      endpoint: "/trig/basic",
      operations: ["sin", "cos", "tan", "sec", "csc", "cot", "arcsin", "arccos", "arctan"],
      fields: [{ name: "value", label: "Value / Angle", type: "number" }],
    },
    lawOfSines: {
      endpoint: "/trig/law-of-sines",
      operations: ["solve_side", "solve_angle"],
      fields: [
        { name: "known_side", label: "Known Side", type: "number" },
        { name: "known_angle", label: "Known Angle", type: "number" },
        { name: "target_value", label: "Target Value", type: "number" },
      ],
    },
    lawOfCosines: {
      endpoint: "/trig/law-of-cosines",
      operations: ["solve_side", "solve_angle"],
      fields: [
        { name: "side1", label: "Side 1", type: "number" },
        { name: "side2", label: "Side 2", type: "number" },
        { name: "value3", label: "Angle or Side 3", type: "number" },
      ],
    },
    triangleHelpers: {
      endpoint: "/trig/triangle-helpers",
      operations: ["hypotenuse", "leg", "third_angle"],
      fields: [
        { name: "value1", label: "Value 1", type: "number" },
        { name: "value2", label: "Value 2", type: "number" },
      ],
    },
    unitCircle: {
      endpoint: "/trig/unit-circle",
      operations: ["coordinates", "quadrant"],
      fields: [{ name: "angle", label: "Angle", type: "number" }],
    },
  },
  expressions: {
    manipulate: {
      endpoint: "/expressions/manipulate",
      operations: ["simplify", "expand", "factor"],
      fields: [{ name: "expr", label: "Expression", type: "text" }],
    },
    evaluate: {
      endpoint: "/expressions/evaluate",
      operations: ["evaluate"],
      fields: [{ name: "expr", label: "Expression", type: "text" }],
    },
    equations: {
      endpoint: "/expressions/solve/equation",
      operations: ["linear_equation", "equation"],
      fields: [
        { name: "left_hand", label: "Left Side", type: "text" },
        { name: "right_hand", label: "Right Side", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
      ],
    },
    quadratic: {
      endpoint: "/expressions/solve/quadratic",
      operations: ["quadratic_equation"],
      fields: [
        { name: "value1", label: "a", type: "number" },
        { name: "value2", label: "b", type: "number" },
        { name: "value3", label: "c", type: "number" },
      ],
    },
    system: {
      endpoint: "/expressions/solve/system",
      operations: ["system"],
      fields: [
        { name: "equations", label: "Equations", type: "arrayText" },
        { name: "variables", label: "Variables", type: "arrayText" },
      ],
    },
    roots: {
      endpoint: "/expressions/solve/roots",
      operations: ["roots"],
      fields: [
        { name: "expr", label: "Expression", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
      ],
    },
    derivative: {
      endpoint: "/expressions/calculus/derivative",
      operations: ["derivative"],
      fields: [
        { name: "expr", label: "Expression", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
        { name: "order", label: "Order", type: "number" },
      ],
    },
    integral: {
      endpoint: "/expressions/calculus/integral",
      operations: ["integral"],
      fields: [
        { name: "expr", label: "Expression", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
        { name: "lower_bound", label: "Lower Bound", type: "text" },
        { name: "upper_bound", label: "Upper Bound", type: "text" },
      ],
    },
    limit: {
      endpoint: "/expressions/calculus/limit",
      operations: ["limit"],
      fields: [
        { name: "expr", label: "Expression", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
        { name: "value", label: "Approach Value", type: "text" },
      ],
    },
    domain: {
      endpoint: "/expressions/function/domain",
      operations: ["domain"],
      fields: [
        { name: "expr", label: "Expression", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
      ],
    },
    intercepts: {
      endpoint: "/expressions/function/intercepts",
      operations: ["intercepts"],
      fields: [{ name: "expr", label: "Expression", type: "text" }],
    },
    criticalPoints: {
      endpoint: "/expressions/function/critical-points",
      operations: ["critical_points", "local_extrema"],
      fields: [
        { name: "expr", label: "Expression", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
      ],
    },
    inflectionPoints: {
      endpoint: "/expressions/function/inflection-points",
      operations: ["inflection_points"],
      fields: [
        { name: "expr", label: "Expression", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
      ],
    },
  },
  stats: {
    singleArray: {
      endpoint: "/stats/single-array",
      operations: ["mean", "median", "mode", "range", "quartiles", "iqr"],
      fields: [{ name: "data", label: "Dataset", type: "array" }],
    },
    arrayScalar: {
      endpoint: "/stats/array-scalar",
      operations: ["variance", "std", "percentile"],
      fields: [
        { name: "data", label: "Dataset", type: "array" },
        { name: "value", label: "Value", type: "number" },
      ],
    },
    twoArrays: {
      endpoint: "/stats/two-arrays",
      operations: ["covariance", "correlation"],
      fields: [
        { name: "dataset_1", label: "Dataset 1", type: "array" },
        { name: "dataset_2", label: "Dataset 2", type: "array" },
      ],
    },
    combinatorics: {
      endpoint: "/stats/combinatorics",
      operations: ["permutations", "combinations"],
      fields: [
        { name: "total_items", label: "Total Items", type: "number" },
        { name: "selected_items", label: "Selected Items", type: "number" },
      ],
    },
    zScore: {
      endpoint: "/stats/z-score",
      operations: ["z_score"],
      fields: [
        { name: "value", label: "Value", type: "number" },
        { name: "mean", label: "Mean", type: "number" },
        { name: "standard_deviation", label: "Std Dev", type: "number" },
      ],
    },
  },
  geometry2d: {
    singleInput: {
      endpoint: "/geometry-2d/single-input",
      operations: ["square_area", "square_perimeter", "square_diagonal", "circle_area", "circle_circumference"],
      fields: [{ name: "value", label: "Value", type: "number" }],
    },
    twoInput: {
      endpoint: "/geometry-2d/two-input",
      operations: [
        "rectangle_area",
        "rectangle_perimeter",
        "rectangle_diagonal",
        "triangle_area_right",
        "triangle_area_isosceles",
        "parallelogram_area",
        "parallelogram_perimeter",
      ],
      fields: [
        { name: "value1", label: "Value 1", type: "number" },
        { name: "value2", label: "Value 2", type: "number" },
      ],
    },
    threeInput: {
      endpoint: "/geometry-2d/three-input",
      operations: ["triangle_area_sss", "triangle_perimeter", "trapezoid_area"],
      fields: [
        { name: "value1", label: "Value 1", type: "number" },
        { name: "value2", label: "Value 2", type: "number" },
        { name: "value3", label: "Value 3", type: "number" },
      ],
    },
    trapezoidPerimeter: {
      endpoint: "/geometry-2d/trapezoid-perimeter",
      operations: ["trapezoid_perimeter"],
      fields: [
        { name: "side1", label: "Side 1", type: "number" },
        { name: "side2", label: "Side 2", type: "number" },
        { name: "side3", label: "Side 3", type: "number" },
        { name: "side4", label: "Side 4", type: "number" },
      ],
    },
    polygon: {
      endpoint: "/geometry-2d/polygon",
      operations: [
        "regular_polygon_area",
        "regular_polygon_perimeter",
        "polygon_interior_angle_sum",
        "regular_polygon_interior_angle",
      ],
      fields: [
        { name: "sides", label: "Sides", type: "number" },
        { name: "side_length", label: "Side Length", type: "numberOptional" },
      ],
    },
  },
  geometry3d: {
    singleInput: {
      endpoint: "/geometry-3d/single-input",
      operations: ["cube_volume", "cube_surface_area", "cube_edge_sum", "sphere_volume", "sphere_surface_area"],
      fields: [{ name: "value", label: "Value", type: "number" }],
    },
    twoInput: {
      endpoint: "/geometry-3d/two-input",
      operations: [
        "cylinder_volume",
        "cylinder_surface_area",
        "cone_slant_height",
        "cone_volume",
        "cone_surface_area",
        "pyramid_volume",
      ],
      fields: [
        { name: "value1", label: "Value 1", type: "number" },
        { name: "value2", label: "Value 2", type: "number" },
      ],
    },
    threeInput: {
      endpoint: "/geometry-3d/three-input",
      operations: ["prism_volume", "prism_surface_area", "prism_diagonal"],
      fields: [
        { name: "value1", label: "Value 1", type: "number" },
        { name: "value2", label: "Value 2", type: "number" },
        { name: "value3", label: "Value 3", type: "number" },
      ],
    },
  },
  linear: {
    vectorPair: {
      endpoint: "/linear/vector-pair",
      operations: ["vector_add", "vector_subtract", "vector_dot_product", "vector_cross_product"],
      fields: [
        { name: "vector_1", label: "Vector 1", type: "array" },
        { name: "vector_2", label: "Vector 2", type: "array" },
      ],
    },
    vectorSingle: {
      endpoint: "/linear/vector-single",
      operations: ["vector_magnitude", "vector_unit"],
      fields: [{ name: "vector", label: "Vector", type: "array" }],
    },
    vectorScalar: {
      endpoint: "/linear/vector-scalar",
      operations: ["vector_scalar_multiply"],
      fields: [
        { name: "vector", label: "Vector", type: "array" },
        { name: "scalar", label: "Scalar", type: "number" },
      ],
    },
    matrixPair: {
      endpoint: "/linear/matrix-pair",
      operations: ["matrix_add", "matrix_subtract", "matrix_multiply"],
      fields: [
        { name: "matrix_1", label: "Matrix 1", type: "matrix" },
        { name: "matrix_2", label: "Matrix 2", type: "matrix" },
      ],
    },
    matrixSingle: {
      endpoint: "/linear/matrix-single",
      operations: [
        "matrix_transpose",
        "matrix_determinant",
        "matrix_inverse",
        "matrix_trace",
        "matrix_rank",
        "matrix_eigenvalues",
        "matrix_eigenvectors",
        "matrix_svd",
      ],
      fields: [{ name: "matrix", label: "Matrix", type: "matrix" }],
    },
    matrixScalar: {
      endpoint: "/linear/matrix-scalar",
      operations: ["matrix_scalar_multiply"],
      fields: [
        { name: "matrix", label: "Matrix", type: "matrix" },
        { name: "scalar", label: "Scalar", type: "number" },
      ],
    },
    solveSystem: {
      endpoint: "/linear/solve-system",
      operations: ["solve_linear_system"],
      fields: [
        { name: "coefficient_matrix", label: "Coefficient Matrix", type: "matrix" },
        { name: "constant_vector", label: "Constant Vector", type: "array" },
      ],
    },
  },
  plot: {
    function: {
      endpoint: "/plot/function",
      operations: ["function", "critical_points", "extrema", "inflections"],
      fields: [
        { name: "expr", label: "Expression", type: "text" },
        { name: "variable", label: "Variable", type: "text" },
      ],
    },
    dataset: {
      endpoint: "/plot/dataset",
      operations: ["histogram", "boxplot"],
      fields: [{ name: "data", label: "Dataset", type: "array" }],
    },
    scatter: {
      endpoint: "/plot/scatter",
      operations: ["scatter"],
      fields: [
        { name: "x_data", label: "X Data", type: "array" },
        { name: "y_data", label: "Y Data", type: "array" },
      ],
    },
    vectors: {
      endpoint: "/plot/vectors",
      operations: ["vectors"],
      fields: [{ name: "vector_list", label: "Vectors", type: "matrix" }],
    },
  },
};

export const categoryDefaults = {
  arithmetic: "binary",
  trig: "basic",
  expressions: "manipulate",
  stats: "singleArray",
  geometry2d: "singleInput",
  geometry3d: "singleInput",
  linear: "vectorPair",
  plot: "function",
};

export const categories = [
  { id: "arithmetic", label: "Arithmetic" },
  { id: "trig", label: "Trigonometry" },
  { id: "expressions", label: "Expressions" },
  { id: "stats", label: "Statistics" },
  { id: "geometry2d", label: "Geometry 2D" },
  { id: "geometry3d", label: "Geometry 3D" },
  { id: "linear", label: "Linear Algebra" },
  { id: "plot", label: "Plotting" },
];
