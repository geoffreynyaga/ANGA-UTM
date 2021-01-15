export interface GeojsonType {
    type: "Polygon" | "Point" | "MultiPoint" | "LineString" | "MultiLineString" | "MultiPolygon" | "GeometryCollection" | "Feature" | "FeatureCollection";
    features: Feature[];
}

export interface Feature {
    id: number;
    type: "Polygon" | "Point" | "MultiPoint" | "LineString" | "MultiLineString" | "MultiPolygon" | "GeometryCollection" | "Feature" | "FeatureCollection";
    geometry: GeometryType;
    properties: Properties;
}

export interface GeometryType {
    type: "Polygon" | "Point" | "MultiPoint" | "LineString" | "MultiLineString" | "MultiPolygon" | "GeometryCollection" | "Feature" | "FeatureCollection";
    coordinates: Array<Array<number[]>>;
}

export interface Properties {
    user_full_name: string;
    user_phone_number: string;
    user_profile_pic: string;
    user_organization: string;
    created_by: number;
    rpas_name: string;
    rpas_serial: string;
    rpas_pic: string;
    airframe_type: string;
    start_day: Date;
    start_time: string;
    start_datetime: Date;
    end: string;
    mission_type_display: string;
    area: number;
    application_number: null | string;
    status: number;
    expiry: boolean;
    centroid: Centroid;
}

export interface Centroid {
    type: string;
    coordinates: number[];
}