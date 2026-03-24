export interface TerrainComponent {
  name: string;
  percentage: number;
  color: string;
}

export interface TerrainAnalysis {
  is_terrain: boolean;
  terrain_type: string;
  components: TerrainComponent[];
  fertile_areas: string[];
  technical_report: string;
  recommendations: string[];
  overall_fertility_score: number;
}

export interface Analysis {
  id: number;
  filename: string;
  original_image: string;
  heatmap_image: string | null;
  analysis_result: TerrainAnalysis;
  created_at: string;
}
