namespace RBBH.CollateralAppraisal.Application.Branches;

public record CityDto(int Id, string Name);

public record BranchDto(int Id, string Code, string Name, string Address, int CityId, string CityName);
