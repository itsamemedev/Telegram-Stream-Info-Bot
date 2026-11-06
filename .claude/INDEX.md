# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10188  GET              /                                                dashboard
 12243  GET              /api/abo/status                                  api_abo_status
 12197  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10976  GET              /api/automation/status                           api_automation_status
 10998  POST             /api/automation/toggle                           api_automation_toggle
 19849  GET              /api/channel/categories                          api_channel_categories
 19855  POST             /api/channel/set                                 api_channel_set
 19702  GET              /api/channels/status                             api_channels_status
 19376  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19359  GET              /api/clips                                       api_clips
 19405  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19277  GET              /api/debug/threads                               api_debug_threads
 12208  GET              /api/events                                      api_events
 11687  GET              /api/events/stream                               api_events_stream
 11514  GET              /api/health                                      api_health
 19318  POST             /api/highlights/config                           api_highlights_config
 10122  POST             /api/login                                       dashboard_login_submit
 12533  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11602  GET              /api/notify/status                               api_notify_status
 11613  POST             /api/notify/test                                 api_notify_test
 12297  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12274  GET              /api/proxy/trend                                 api_proxy_trend
 19425  GET              /api/tts/<fn>                                    api_tts_file
 20202  GET              /api/upload_window                               api_upload_window
 11804  GET              /archive/<int:eid>/download                      archive_download
 11832  GET              /download/<int:recording_id>                     download
 11761  GET              /health                                          health
 19186  GET              /healthz                                         healthz
 10113  GET              /login                                           dashboard_login_page
 10143  GET              /logout                                          dashboard_logout
 10150  GET              /manifest.webmanifest                            pwa_manifest
 20175  GET              /overlay                                         overlay_page
 10174  GET              /pwa-icon-<variant>.png                          pwa_icon
 10160  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   509  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   526  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   578  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   600  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   539  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   565  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   239  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   460  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   489  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   409  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   422  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   518  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   395  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   270  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   315  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   339  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   326  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   166  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   284  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   136  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   376  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   431  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (66)

```
  2091  /about                  Ueber diesen Bot
   813  /ai                     
  2091  /aireset                KI-Kontext zuruecksetzen
  1222  /ask                    
   914  /assign_role            
   964  /ban                    
  2046  /botstats               
  2091  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2091  /bulkadd                Mehrere User auf einmal tracken · a b c
  2091  /cleanup                Alte Aufnahmen aufraeumen
  1477  /clearwarns             
  2010  /clip                   
  1995  /clipoftheweek          
  1348  /clips                  
  2091  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   869  /create_category        
   840  /create_channel         
   904  /create_group           
   879  /create_role            
   855  /create_voice           
  1100  /daily                  
  2091  /diag                   Vollstaendige Diagnose
  2091  /einnahmen              Einnahmen und Spenden
  1251  /event                  
  1293  /events                 
  1387  /follow                 
  1376  /help                   
   954  /kick                   
  1075  /leaderboard            
  2091  /live                   Live-Status sofort pruefen · @user
  1335  /livenow                
  2091  /logs                   Letzte Fehler aus dem Log
  2091  /pause                  Tracking pausieren · @user
  1363  /post_test              
  1183  /profile                
   986  /purge                  
  2091  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2091  /quota                  Speicher-Quota
  1062  /rank                   
  1323  /recstatus              
   924  /remove_role            
  2091  /report                 Azrael-Sentinel-Wochenreport
   826  /restream_status        
  2091  /resume                 Tracking fortsetzen · @user
   934  /set_channel_perms      
  1029  /setup_community        
  1046  /setup_targets          
  1419  /stats                  
   785  /status                 
  2091  /stoprec                Laufende Aufnahme sauber beenden · @user
  1515  /streaminfo             
  2091  /summary                Tageszusammenfassung
  2091  /sysres                 System-Ressourcen
  2091  /teststream             Recorder-Selbsttest · @user
  2091  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   974  /timeout                
  1487  /topstreamers           
  2091  /topusers               Top-Streamer nach Aufnahmen
   715  /track                  
  2091  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   798  /tracklist              
  1401  /unfollow               
  2091  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   747  /untrack                
  1440  /warn                   
  1463  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2249  on_member_join
  2211  on_message
  2112  on_raw_reaction_add
  2284  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-476    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1592-1643   _award_xp
  1814-1843   _clip_week_leader
  1867-1881   _clipoftheweek_loop
  2400-2462   _community_events_loop
  1549-1571   _dc_client
  1574-1583   _dc_offen
  2502-2537   _disc_automod_check
   403-408    _disc_sprache_setzen
  1646-1694   _discord_ai_automod
   536-575    _discord_automod
  1697-1717   _discord_azrael_reply
  1884-2359   _discord_run_once
   238-296    _discord_start
   299-353    _ensure_discord_invite
  2365-2397   _ensure_error_channel
   424-437    _ensure_rank_roles
   678-692    _ensure_team_roles
  2465-2495   _error_channel_loop
   585-589    _guard
   505-533    _handle_voice_ai
   411-421    _is_admin
  1762-1773   _liveboard_loop
   592-610    _on_level_up
   501-502    _par_chat_id
  1846-1864   _post_clip_of_week
  1776-1794   _post_weekly_digest
   440-466    _provision_base_channels
   469-485    _provision_user_channels
  1315-1408   _reg_betrieb
  1000-1089   _reg_community_setup
  1092-1172   _reg_daily_profil
  1215-1312   _reg_frage_events
   772-828    _reg_info
   946-997    _reg_moderation
  1175-1212   _reg_profil
   895-943    _reg_rollen
   831-892    _reg_server
  1411-1498   _reg_streamer
  1501-1546   _reg_system
   706-769    _reg_tracking
   645-675    _run_tg_handler
   488-498    _tracked_usernames
   155-217    _uebernehmen
  1726-1759   _update_liveboard
  1797-1811   _weekly_digest_loop
   220-223    starte
```

## Top-Level-Symbole in bot.py (543 Funktionen, 2 Klassen)

```
 25097-25119  _abbruch_datenbank_unlesbar
  2663-2664   _abo_key
  2684-2702   _abo_probe_dump
 25215-25231  _abschied_wachen
 25234-25252  _abschluss
 16070-16077  _ad_allowlist
 17069-17075  _agent_for
 17078-17094  _ai_telemetry
 17591-17609  _alert
 21070-21120  _alert_monitor_loop
 21502-21564  _announce_loop
  3549-3559   _anthropic_key
  3566-3568   _anthropic_model
  9788-9791   _arg_int
  2655-2660   _as_dict
 24802-24811  _async_exc_handler
 17772-17794  _audio_tap_cmd
 18352-18411  _audio_tap_melden
 17808-17832  _audio_tap_sammler
  9137-9170   _aufnahme_beim_stopp_sichern
 24051-24053  _aufnahme_deckel
  9173-9191   _aufnahme_platz_frei
 25179-25199  _aufnahmen_abschliessen
 25122-25176  _aufraeumen
  9976-10045  _auth_cookie
  9934-9972   _auth_guard
  1905-1910   _auto_on
 19038-19056  _auto_restream_loop
 13745-13787  _avatar_frames_laden
 22585-22600  _azrael_broadcast_reply
 22485-22507  _azrael_chat_reply
 22457-22482  _azrael_chat_should_reply
 22513-22515  _azrael_gate_cfg
 17099-17113  _azrael_live_state
 20088-20102  _azrael_overlay_state
 17473-17527  _azrael_proactive_loop
 16917-16973  _azrael_reaction_to_chats
 22518-22525  _azrael_reply_all_chats
 22444-22454  _azrael_self_names
 22553-22582  _azrael_send_to
 13706-13742  _azrael_spricht
 14049-14062  _azrael_stimme_stumm
 17119-17140  _azrael_system
 21204-21207  _backup_active
 21285-21298  _backup_loop
 24140-24144  _betrieb
 24875-24884  _brain_crowdsec_snap
 25024-25027  _brain_db_health
 20991-21000  _brain_growth_loop
 10367-10394  _brain_growth_snapshot
  2588-2608   _brain_hint_delay
 24947-24982  _brain_moderation_snap
  6492-6520   _brain_notify
 25030-25052  _brain_recording_snap
 24887-24944  _brain_restream_health
 25055-25068  _brain_tiktok_status_snap
 11666-11683  _browser_push
  6532-6619   _build_daily_summary
 14096-14100  _build_restream_cmd
  5245-5272   _can_stop_tracking
  2018-2040   _capture_set_cookies
 12351-12354  _cfg_get
 12357-12359  _cfg_set
 19810-19845  _channel_set_all
 12934-12937  _chat_connected
 12940-12956  _chat_disconnected
  8780-8791   _chat_is_forum
 18159-18184  _chat_listener_abbauen
 12976-12978  _chat_sanitize
 12919-12931  _chat_stat
 12959-12962  _chat_stats_snapshot
  3867-3879   _check_ai_models_sync
 10649-10692  _classify_pool_anonymity
 10695-10712  _classify_pool_anonymity_bg
   896-918    _claude_chat_sync_metered
  9820-9826   _client_ip
 21648-21675  _clip_prune
 21678-21688  _clip_recfile_for
 22101-22107  _clip_should_velocity
 21730-21812  _clip_to_discord
  3753-3762   _close_ai_session
 22631-22646  _cohost_broadcast
 22616-22617  _cohost_cfg
 22672-22684  _cohost_fire_highlight
 22620-22628  _cohost_gate
 22649-22669  _cohost_highlight
 10297-10299  _conv_messages
  6891-6952   _cookie_alarm_loop
  2108-2109   _cookie_autofetch_info
  2092-2096   _cookie_autorefresh_info
 24509-24531  _cookie_bezug_loop
 24534-24559  _cookie_bezug_runde
  1995-1999   _cookie_header
  2121-2135   _cookies_selbst_holen
  4083-4085   _create_index_safe
 20534-20648  _crowdsec_status
 20480-20531  _crowdsec_via_lapi
 20384-20402  _cscli_bin
 20411-20424  _cscli_path
  6781-6806   _daily_summary_loop
 20442-20459  _darf_journal_lesen
  3078-3103   _darf_ytdlp_nachschlagen
 11847-11868  _dashboard_adresse
 21044-21067  _db_maintenance_loop
  6750-6778   _db_vacuum_loop
 16093-16117  _detect_foreign_ad
  1585-1596   _diag_path_owner
 17378-17423  _director_finalize
 18341-18348  _director_for
 17327-17375  _director_mark
 21964-21967  _disc_state_get
 21970-21977  _disc_state_set
 20972-20981  _discord_bot_starten
 20935-20946  _discord_einladung_merken
 20984-20988  _discord_invite
 20949-20969  _discord_kontext
 21925-21961  _discord_live_thread
 17530-17542  _discord_notify
 20907-20932  _discord_ops_alert
 21823-21921  _discord_post_user
 21567-21573  _discord_stop
  6809-6886   _disk_alarm_loop
 24434-24483  _disk_autoclean
 24657-24670  _disk_guard_loop
 13684-13691  _drossel_hoeher
 13680-13681  _drossel_stufe
 13694-13702  _drossel_zuruecksetzen
 12024-12026  _dump_all_threads
 24147-24161  _einstellungen_startzeile
 10575-10638  _enrich_proxies_with_geo
  2164-2225   _ensure_cookie_file_netscape
  8839-8842   _ensure_notify_topic
 10819-10856  _ensure_proxy_ready
  8793-8820   _ensure_topic
   738-740    _env_int
   743-745    _env_int_range
 17575-17588  _event_webhook
 12702-12715  _evolution_loop
  5934-5968   _extract_file_payload
  2297-2299   _extract_urls_from_streamurl_node
 20427-20434  _f2b_sudo_hint
 25255-25318  _fatal_vom_botteil
 24056-24071  _fd_grenze_anheben
  4709-4719   _fehler_text
 10476-10494  _fetch_proxy_list
 18128-18156  _fetch_tiktok_room_id
   821-824    _ff_cmd
 13513-13518  _find_chromium
  3469-3471   _find_external_recorder
  2302-2304   _find_stream_urls
 12402-12427  _fire_webhooks
  7718-7727   _fork_safe
   929-942    _freeai_chat_sync_metered
 20473-20477  _geo_lookup_ips
  3741-3750   _get_ai_session
  7551-7591   _get_live_info
  2929-2936   _get_resolve_semaphore
  8043-8433   _handle_single_tracking
 24256-24258  _hb
 24261-24278  _hb_while
 12990-12992  _highlight_cfg
 12995-13024  _highlight_observe
 13521-13539  _htmlov_screenshot_cmd
 17834-17844  _httpx_proxy
 12435-12447  _in_quiet_hours
 25083-25094  _init_db_oder_abbruch
 25902-25933  _install_fast_eventloop
  9683-9737   _install_fast_json
 12029-12045  _install_faulthandler
 19089-19098  _intel_ensure_schema
 19141-19176  _intel_index_loop
 19110-19125  _intel_index_one
 19101-19107  _intel_semantic
  5234-5243   _is_authorized
  7929-7950   _is_dead
  2287-2289   _is_hevc
 20462-20464  _is_private_ip
  1804-1811   _is_process_running
  6522-6529   _is_quiet_hours
  1378-1387   _is_upload_window
  4574-4589   _iso
  9829-9835   _ist_lokal
  9772-9785   _json_error_handler
  6744-6745   _kick_broadcaster_id
  6656-6698   _kick_follower_count
  6640-6643   _kick_slug
 11479-11486  _kick_user_token
  7850-7875   _kick_ws_pause
 25071-25080  _kickmod_boot
  4164-4167   _kind_from_filename
 12464-12466  _latest_popularity
  1741-1750   _laufstand
 24617-24654  _laufstand_loop
 24180-24218  _leistung_erheben
 18747-18796  _live_react_loop
 18414-18736  _live_react_worker
  3319-3431   _live_status_aufloesen
 16976-16987  _live_transcript_push
 18738-18745  _live_users
 17426-17470  _living_title_loop
 21210-21282  _local_backup_scan
  9754-9768   _log_5xx
 24221-24253  _log_schleuse_pruefen
   811-818    _log_sicher
 14108-14120  _looks_like_codec_err
 14103-14105  _looks_like_source_expired
  7768-7798   _loop_fehler
 12049-12058  _loop_heartbeat
 23962-23995  _loop_lag_monitor
 24009-24029  _loop_stockung_melden
 24032-24042  _loop_takt_starten
 12061-12134  _loop_watchdog_thread
 16853-16870  _loyalty_add
 16844-16850  _loyalty_get
 16873-16881  _loyalty_top
 12574-12576  _manual_donations_total
  4916-4935   _manual_status
  7952-7953   _mark_dead
 11095-11111  _marketing_loop
 22532-22550  _maybe_handle_command
 24756-24780  _maybe_hype_clip
 21617-21645  _meme_klassifizieren
  4070-4075   _migrate_columns
 22811-22822  _mod_is_exempt
 22825-22830  _mod_warn_first
 22833-22836  _mod_warn_text
 12759-12778  _modlog
 12742-12756  _modlog_schreiben
  1074-1076   _multistream_targets
  3106-3142   _nachschlag_ytdlp
  7730-7731   _nc_create_subprocess_exec
  7734-7735   _nc_create_subprocess_shell
 11416-11433  _news_loop
 12801-12803  _normalize_ingest
  2519-2536   _note_check_duration
  8833-8836   _notify_topic_name
  3145-3165   _ohne_url_melden
 17002-17010  _oracle_memories
 17276-17310  _oracle_memorize
 17013-17026  _oracle_persona
 16995-16999  _oracle_recent_text
 13147-13148  _ov_atomic_write
 13138-13140  _ov_bar
 15996-16008  _ov_clip_text
 13143-13144  _ov_oneline
 20139-20168  _overlay_push
 13467-13510  _overlay_render_size
 12870-12874  _overlay_session_reset
 20104-20106  _overlay_src_ok
 16080-16090  _own_invites
 13462-13464  _parse_size
 20656-20736  _parse_ssh_attacks
  7153-7186   _pause_resume_cmd
  2046-2090   _persist_refreshed_cookies
  1949-1981   _pick_checked_pull_proxy
  9864-9877   _pin_auth_value
  9923-9924   _pin_clear_fail
  9903-9906   _pin_locked
  9909-9920   _pin_note_fail
  9880-9900   _pin_ok
 19946-19971  _piper_pick_model
 20031-20082  _piper_say
 12364-12399  _post_json_threaded
 13441-13459  _probe_video_size
  1832-1849   _proc_is_recorder
 10788-10816  _proxy_pool_refresh_loop
  1915-1946   _proxy_report_recording
  8531-8569   _pruefstand_melden
 24091-24102  _pruefung_verworfen
 12014-12016  _prune_stall_dumps
 11165-11335  _public_stats
  2112-2118   _pull_proxy_still
 17546-17572  _push_notify
 10092-10094  _pwa_dir
 10545-10560  _quick_validate_proxy
 12430-12432  _quiet_hours_config
 10057-10090  _rate_guard
 16814-16820  _react_warn
  7638-7677   _reap_proc
  9067-9134   _rec_auto_abschalten
  9014-9064   _rec_frueh_getrennt
  8897-8959   _rec_kategorie_melden
  8962-9011   _rec_totstreak_fortschreiben
  2559-2581   _record_check_outcome
   806-808    _redact_stream_urls
 10715-10785  _refresh_proxy_pool
  2336-2427   _resolve_via_html
  2709-2906   _resolve_via_webcast_api_v2
  2969-3054   _resolve_via_ytdlp
 22141-22270  _resolve_youtube_ingest
  2313-2333   _resolver_stumm
 12853-12864  _restream_active_sources
 13790-13914  _restream_avatar_feeder_start
 13917-13926  _restream_avatar_feeder_stop
 18187-18305  _restream_chat_guardian
 13027-13099  _restream_chat_push
 13124-13133  _restream_chat_push_async
 24985-25021  _restream_durchreicher
 13542-13651  _restream_html_overlay_start
 13654-13667  _restream_html_overlay_stop
 12812-12835  _restream_overlay_files
 18800-18832  _restream_platform_state
 19000-19035  _restream_resume_after_restart
 13974-14046  _restream_tts_enqueue_wav
 13403-13435  _restream_tts_feeder
 13400-13401  _restream_tts_fifo_path
 13929-13956  _restream_tts_start
 13958-13972  _restream_tts_stop
 18838-18997  _restream_verify_loop
 21175-21187  _retention_loop
 21169-21172  _retention_scan
  2666-2668   _room_is_abo
  5972-6089   _run_ai_call
 12157-12170  _run_async_from_flask
 20467-20470  _run_priv
 25890-25898  _run_selfcheck_and_exit
 21190-21201  _s3_client
  7979-8030   _safe_send
  4842-4858   _sample_net_throughput
  2611-2641   _schedule_next_check
 21123-21166  _scheduler_loop
  4078-4080   _schema_pk
 12174-12179  _scraper_session
 22839-22878  _screen_full
 11530-11567  _sec_headers
  2292-2294   _select_stream_from_data_section
 25610-25887  _selfcheck
  8845-8879   _send_live_notice
  1401-1405   _should_defer_upload
 21691-21727  _shrink_for_discord
 10097-10109  _sicheres_ziel
 21003-21041  _sicherheits_erinnerung_loop
 24677-24694  _sign_health_check
 24697-24716  _sign_health_loop
  4592-4617   _sitzung_bestimmen
  7747-7758   _spawn
 26315-26345  _spawn_from_flask
 24105-24111  _speicher_maps
 24114-24129  _speicher_pflegen
 17846-18125  _start_chat_listener
 24074-24088  _start_gesperrt
 12137-12154  _start_loop_watchdog
 11362-11411  _stats_loop
 11341-11344  _stats_output_path
 11347-11359  _stats_write
 19983-19997  _stimme_saubern
 20004-20028  _stimme_schon_gesagt
  8512-8528   _storage_cleanup_loop
 24736-24743  _story_for
  3494-3500   _stream_url_expiry
  3502-3507   _stream_url_ttl
 16043-16050  _streamer_persona_get
 21307-21459  _system_backup
 21468-21498  _system_backup_loop
 11974-11992  _task_auf_bot_schleife
 23652-23668  _telegram_befehlsmenue
  7801-7847   _telegram_polling_fehler
 10497-10536  _test_proxy
 11043-11059  _testpush_resolve_live
  7955-7976   _tg_sprache_setzen
  8752-8762   _tg_topics_load_into_mem
  8749-8750   _tg_topics_path
  8764-8771   _tg_topics_save
  9838-9846   _token_ok
  8774-8778   _topic_forget
 12450-12461  _tracking_max_duration
  4372-4386   _tracking_remove_cleanup
  4403-4415   _tracking_resume_cleanup
  1643-1666   _try_attach_file_handler
 19973-19981  _tts_cleanup
 11019-11023  _tunnel_effective
 24486-24506  _tunnel_lage
 24562-24614  _tunnel_wacht_loop
 19469-19522  _twitch_channel_status
 22881-23026  _twitch_chat_loop
 21983-21996  _twitch_clip_versuchen
 22695-22798  _twitch_eventsub_loop
  1424-1437   _upload_queue_add
  1448-1450   _upload_queue_count
  1407-1416   _upload_queue_load
  1397-1399   _upload_queue_path
  1439-1446   _upload_queue_remove
  1418-1422   _upload_queue_save
  1452-1493   _upload_window_loop
  7611-7618   _uptime_s
 12789-12798  _url_host
  3168-3267   _url_nachschlag
   889-893    _usage_record_claude
 24850-24872  _v37_pause_source
 24814-24824  _v37_restream_restart
 24827-24847  _v37_unpause_source
  7878-7922   _verbindung_verloren
  6701-6732   _viewer_sample_loop
  9927-9930   _wants_html
  7621-7635   _warn_empty_env
 24299-24420  _watchdog_loop
 22416-22424  _wchat_thank_ok
 17614-17644  _whisper_get_model
  7708-7715   _whisper_native_section
 16801-16807  _whisper_pool
 17738-17770  _whisper_segments
 17646-17662  _whisper_stumm
 17665-17735  _whisper_transcribe
 13195-13357  _write_restream_overlay
 13157-13192  _write_restream_overlay_async
 23050-23146  _youtube_api_chat_loop
 19525-19628  _youtube_api_status
 19631-19698  _youtube_channel_status
 23149-23310  _youtube_chat_loop
 21999-22024  _youtube_clip_versuchen
 22276-22289  _youtube_restream_autoconfig
 22292-22316  _youtube_restream_autoconfig_inner
 22383-22411  _youtube_send
 19766-19807  _youtube_set_channel
 22319-22353  _yt_access_token
 22356-22371  _yt_live_chat_id
 22379-22380  _yt_sendrate_cfg
 23029-23044  _yt_timeout
  2953-2954   _ytdlp_detect_available
  2956-2967   _ytdlp_note_result
 12019-12021  _zombie_child_count
 24164-24177  _zustand_kennzahlen
  7487-7511   about
  4283-4287   add_ai_log_entry
  4200-4203   add_archive_entry
  4880-4882   add_archive_rule
  4620-4691   add_recording
  4347-4364   add_tracking
  6092-6125   ai
  3893-3974   ai_chat
  4008-4018   ai_history_append
  4020-4025   ai_history_clear
  3997-4006   ai_history_load
  3982-3995   ai_rate_limit_check
  6154-6162   aireset
 17143-17162  azrael_chat
 23315-23437  brain_cmd
  3510-3515   build_recording_cmd
  4367-4370   bulk_add_trackings
  6955-7014   bulkadd
  8572-8732   check_all_trackings
  4419-4431   claim_live_transition
 16120-16733  class KickModerator
 14123-15883  class RestreamManager
 10902-10944  classify_proxy_anonymity
  6200-6398   cleanup
  5170-5176   cleanup_old_recordings
  4565-4572   clear_recording
 22027-22098  clip_moment
  4832-4835   compute_storage_forecast
  7077-7150   cookies_cmd
  4338-4344   count_trackings_for_chat
  4270-4281   decide_preferred_recorder
  4210-4213   delete_archive_entry
  4884-4886   delete_archive_rule
  5629-5776   diag
 23549-23610  einnahmen_cmd
  4826-4829   find_recordings_by_fingerprint
  4231-4247   finish_recording_attempt
  4391-4393   get_all_active_trackings
  4298-4300   get_all_checks
  4693-4696   get_all_recordings
  4775-4777   get_all_tags_with_counts
  4803-4806   get_annotations_for_recording
  4205-4208   get_archive_entry
  4796-4799   get_bookmarked_recordings
  2152-2157   get_cookie_health
  4763-4769   get_event_log
  4254-4268   get_last_recording_attempt
  3270-3312   get_live_status
  5109-5112   get_manual_recordings
  4811-4814   get_or_compute_inspect_sync
  5211-5214   get_outcome_breakdown
  4782-4785   get_priority_poll_interval
  4249-4252   get_recent_recording_attempts
  4698-4701   get_recording_by_id
  4789-4792   get_recording_note
  3681-3710   get_redis
  4327-4330   get_stats
  5164-5168   get_storage_stats
  4904-4906   get_tiktok_status_distribution
  4433-4442   get_tracking_state
  4388-4389   get_trackings_for_group
  5125-5128   get_trash_recordings
  9194-9662   handle_recording_finished
 23644-23649  hilfe_cmd
  4093-4155   init_db
  4876-4878   list_archive_rules
  5414-5452   live
  8033-8041   live_check_worker
  3765-3804   llm_chat
  3827-3857   llm_chat_sync
  3812-3824   llm_list_models
  4722-4755   log_event
  1766-1799   log_recording_failure
  7300-7349   logs_cmd
 25321-25600  main
  6128-6151   on_ai_media
  7426-7452   on_ai_reply
  7455-7484   on_azrael_mention
  7516-7546   on_callback
 17168-17273  oracle_handle
  7189-7192   pause_tracking
  5224-5229   profile_keyboard
  5367-5411   quelle
  7251-7297   quota
  8435-8509   reaper_loop
  4900-4902   record_tiktok_status
  6167-6197   recstatus
  3712-3720   redis_get_json
  3723-3729   redis_set_json
 23671-23681  report_cmd
 10947-10949  report_proxy_result
  2430-2472   resolve_tiktok_live_stream
  5120-5123   restore_recording
  7195-7198   resume_tracking
  4889-4894   run_archive_rules
 23684-23942  run_bot
 11871-11965  run_flask
  4864-4867   sample_bandwidth_for_active
  4290-4296   save_tiktok_check
  4557-4563   set_recording_file
  4396-4400   set_tracking_paused
  5115-5118   soft_delete_recording
  8885-8895   split_and_send_video
  5277-5319   start
  4215-4229   start_recording_attempt
  6401-6439   stats
  5054-5107   stop_manual_recording
  7201-7248   stoprec
  6625-6633   summary_cmd
  7352-7423   sysres
  5778-5922   teststream
  5321-5362   tiktok
  7017-7074   topusers
  5489-5546   track
  5454-5486   track_exact
  5560-5627   tracklist
  4938-5052   trigger_manual_recording
  4518-4555   try_acquire_recording_lock
  5131-5133   universal_search
 23613-23641  unpause_cmd
  5548-5558   untrack
 23440-23546  update_cmd
  4821-4824   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, uebersicht, vergessen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, ist_telegram_chat, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
