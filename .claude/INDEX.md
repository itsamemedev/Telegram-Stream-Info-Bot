# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9970  GET              /                                                dashboard
 12017  GET              /api/abo/status                                  api_abo_status
 11971  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10758  GET              /api/automation/status                           api_automation_status
 10780  POST             /api/automation/toggle                           api_automation_toggle
 19396  GET              /api/channel/categories                          api_channel_categories
 19402  POST             /api/channel/set                                 api_channel_set
 19249  GET              /api/channels/status                             api_channels_status
 18923  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18906  GET              /api/clips                                       api_clips
 18952  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18824  GET              /api/debug/threads                               api_debug_threads
 11982  GET              /api/events                                      api_events
 11466  GET              /api/events/stream                               api_events_stream
 11293  GET              /api/health                                      api_health
 18865  POST             /api/highlights/config                           api_highlights_config
  9904  POST             /api/login                                       dashboard_login_submit
 12307  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11381  GET              /api/notify/status                               api_notify_status
 11392  POST             /api/notify/test                                 api_notify_test
 12071  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12048  GET              /api/proxy/trend                                 api_proxy_trend
 18972  GET              /api/tts/<fn>                                    api_tts_file
 19747  GET              /api/upload_window                               api_upload_window
 11583  GET              /archive/<int:eid>/download                      archive_download
 11611  GET              /download/<int:recording_id>                     download
 11540  GET              /health                                          health
 18739  GET              /healthz                                         healthz
  9895  GET              /login                                           dashboard_login_page
  9925  GET              /logout                                          dashboard_logout
  9932  GET              /manifest.webmanifest                            pwa_manifest
 19720  GET              /overlay                                         overlay_page
  9956  GET              /pwa-icon-<variant>.png                          pwa_icon
  9942  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (338)

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
   499  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   763  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   645  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   628  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   620  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   807  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   772  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   792  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   679  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
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
   288  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
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
   179  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   490  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   465  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   944  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1053  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1081  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1101  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   931  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   993  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   980  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   961  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   606  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   601  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   649  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   532  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   859  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   623  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   586  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   559  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   833  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   792  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   698  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   631  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   411  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   876  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   499  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   754  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   909  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   894  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   455  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   693  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   679  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   662  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   719  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1244  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1365  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1208  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   812  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   708  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
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
   478  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   342  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   372  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
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
   414  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (65)

```
  2082  /about                  Ueber diesen Bot
   809  /ai                     
  2082  /aireset                KI-Kontext zuruecksetzen
  1213  /ask                    
   910  /assign_role            
   960  /ban                    
  2037  /botstats               
  2082  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2082  /bulkadd                Mehrere User auf einmal tracken · a b c
  2082  /cleanup                Alte Aufnahmen aufraeumen
  1468  /clearwarns             
  2001  /clip                   
  1986  /clipoftheweek          
  1339  /clips                  
  2082  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   865  /create_category        
   836  /create_channel         
   900  /create_group           
   875  /create_role            
   851  /create_voice           
  1096  /daily                  
  2082  /diag                   Vollstaendige Diagnose
  2082  /einnahmen              Einnahmen und Spenden
  1242  /event                  
  1284  /events                 
  1378  /follow                 
  1367  /help                   
   950  /kick                   
  1071  /leaderboard            
  2082  /live                   Live-Status sofort pruefen · @user
  1326  /livenow                
  2082  /logs                   Letzte Fehler aus dem Log
  2082  /pause                  Tracking pausieren · @user
  1354  /post_test              
  1174  /profile                
   982  /purge                  
  2082  /quota                  Speicher-Quota
  1058  /rank                   
  1314  /recstatus              
   920  /remove_role            
  2082  /report                 Azrael-Sentinel-Wochenreport
   822  /restream_status        
  2082  /resume                 Tracking fortsetzen · @user
   930  /set_channel_perms      
  1025  /setup_community        
  1042  /setup_targets          
  1410  /stats                  
   781  /status                 
  2082  /stoprec                Laufende Aufnahme sauber beenden · @user
  1506  /streaminfo             
  2082  /summary                Tageszusammenfassung
  2082  /sysres                 System-Ressourcen
  2082  /teststream             Recorder-Selbsttest · @user
  2082  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   970  /timeout                
  1478  /topstreamers           
  2082  /topusers               Top-Streamer nach Aufnahmen
   711  /track                  
  2082  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   794  /tracklist              
  1392  /unfollow               
  2082  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   743  /untrack                
  1431  /warn                   
  1454  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2240  on_member_join
  2202  on_message
  2103  on_raw_reaction_add
  2275  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1583-1634   _award_xp
  1805-1834   _clip_week_leader
  1858-1872   _clipoftheweek_loop
  2391-2453   _community_events_loop
  1540-1562   _dc_client
  1565-1574   _dc_offen
  2493-2528   _disc_automod_check
   401-406    _disc_sprache_setzen
  1637-1685   _discord_ai_automod
   534-573    _discord_automod
  1688-1708   _discord_azrael_reply
  1875-2350   _discord_run_once
   236-294    _discord_start
   297-351    _ensure_discord_invite
  2356-2388   _ensure_error_channel
   422-435    _ensure_rank_roles
   674-688    _ensure_team_roles
  2456-2486   _error_channel_loop
   583-587    _guard
   503-531    _handle_voice_ai
   409-419    _is_admin
  1753-1764   _liveboard_loop
   590-608    _on_level_up
   499-500    _par_chat_id
  1837-1855   _post_clip_of_week
  1767-1785   _post_weekly_digest
   438-464    _provision_base_channels
   467-483    _provision_user_channels
  1306-1399   _reg_betrieb
   996-1085   _reg_community_setup
  1088-1163   _reg_daily_profil
  1206-1303   _reg_frage_events
   768-824    _reg_info
   942-993    _reg_moderation
  1166-1203   _reg_profil
   891-939    _reg_rollen
   827-888    _reg_server
  1402-1489   _reg_streamer
  1492-1537   _reg_system
   702-765    _reg_tracking
   643-671    _run_tg_handler
   486-496    _tracked_usernames
   153-215    _uebernehmen
  1717-1750   _update_liveboard
  1788-1802   _weekly_digest_loop
   218-221    starte
```

## Top-Level-Symbole in bot.py (532 Funktionen, 2 Klassen)

```
 24507-24529  _abbruch_datenbank_unlesbar
  2635-2636   _abo_key
  2656-2674   _abo_probe_dump
 24622-24640  _abschluss
 15657-15664  _ad_allowlist
 16637-16643  _agent_for
 16646-16662  _ai_telemetry
 17159-17177  _alert
 20607-20657  _alert_monitor_loop
 21009-21071  _announce_loop
  3514-3524   _anthropic_key
  3531-3533   _anthropic_model
  9587-9590   _arg_int
  2627-2632   _as_dict
 24257-24266  _async_exc_handler
 17340-17362  _audio_tap_cmd
 17920-17979  _audio_tap_melden
 17376-17400  _audio_tap_sammler
  8968-9001   _aufnahme_beim_stopp_sichern
 23557-23559  _aufnahme_deckel
 24589-24609  _aufnahmen_abschliessen
 24532-24586  _aufraeumen
  9758-9827   _auth_cookie
  9725-9754   _auth_guard
  1880-1885   _auto_on
 18596-18614  _auto_restream_loop
 13487-13529  _avatar_frames_laden
 22092-22107  _azrael_broadcast_reply
 21992-22014  _azrael_chat_reply
 21964-21989  _azrael_chat_should_reply
 22020-22022  _azrael_gate_cfg
 16667-16681  _azrael_live_state
 19633-19647  _azrael_overlay_state
 17041-17095  _azrael_proactive_loop
 16485-16541  _azrael_reaction_to_chats
 22025-22032  _azrael_reply_all_chats
 21951-21961  _azrael_self_names
 22060-22089  _azrael_send_to
 13448-13484  _azrael_spricht
 13791-13804  _azrael_stimme_stumm
 16687-16708  _azrael_system
 20741-20744  _backup_active
 20822-20835  _backup_loop
 23646-23650  _betrieb
 24330-24339  _brain_crowdsec_snap
 20528-20537  _brain_growth_loop
 10149-10176  _brain_growth_snapshot
  2563-2583   _brain_hint_delay
 24402-24437  _brain_moderation_snap
  6410-6438   _brain_notify
 24440-24462  _brain_recording_snap
 24342-24399  _brain_restream_health
 24465-24478  _brain_tiktok_status_snap
 11445-11462  _browser_push
  6450-6537   _build_daily_summary
 13838-13842  _build_restream_cmd
  5232-5259   _can_stop_tracking
  1993-2015   _capture_set_cookies
 12125-12128  _cfg_get
 12131-12133  _cfg_set
 19357-19392  _channel_set_all
 12676-12679  _chat_connected
 12682-12698  _chat_disconnected
  8611-8622   _chat_is_forum
 17727-17752  _chat_listener_abbauen
 12718-12720  _chat_sanitize
 12661-12673  _chat_stat
 12701-12704  _chat_stats_snapshot
  3826-3838   _check_ai_models_sync
 10431-10474  _classify_pool_anonymity
 10477-10494  _classify_pool_anonymity_bg
   876-898    _claude_chat_sync_metered
  9619-9626   _client_ip
 21155-21182  _clip_prune
 21185-21195  _clip_recfile_for
 21608-21614  _clip_should_velocity
 21237-21319  _clip_to_discord
  3712-3721   _close_ai_session
 22138-22153  _cohost_broadcast
 22123-22124  _cohost_cfg
 22179-22191  _cohost_fire_highlight
 22127-22135  _cohost_gate
 22156-22176  _cohost_highlight
 10079-10081  _conv_messages
  6809-6870   _cookie_alarm_loop
  2083-2084   _cookie_autofetch_info
  2067-2071   _cookie_autorefresh_info
 23967-23989  _cookie_bezug_loop
 23992-24017  _cookie_bezug_runde
  1970-1974   _cookie_header
  2096-2110   _cookies_selbst_holen
  4062-4074   _create_index_safe
 20079-20185  _crowdsec_status
 20025-20076  _crowdsec_via_lapi
 19929-19947  _cscli_bin
 19956-19969  _cscli_path
  6699-6724   _daily_summary_loop
 19987-20004  _darf_journal_lesen
  3048-3073   _darf_ytdlp_nachschlagen
 11626-11647  _dashboard_adresse
 20581-20604  _db_maintenance_loop
  6668-6696   _db_vacuum_loop
 15680-15704  _detect_foreign_ad
  1561-1572   _diag_path_owner
 16946-16991  _director_finalize
 17909-17916  _director_for
 16895-16943  _director_mark
 21471-21474  _disc_state_get
 21477-21484  _disc_state_set
 20509-20518  _discord_bot_starten
 20472-20483  _discord_einladung_merken
 20521-20525  _discord_invite
 20486-20506  _discord_kontext
 21432-21468  _discord_live_thread
 17098-17110  _discord_notify
 20444-20469  _discord_ops_alert
 21330-21428  _discord_post_user
 21074-21080  _discord_stop
  6727-6804   _disk_alarm_loop
 23892-23941  _disk_autoclean
 24112-24125  _disk_guard_loop
 13426-13433  _drossel_hoeher
 13422-13423  _drossel_stufe
 13436-13444  _drossel_zuruecksetzen
 11803-11805  _dump_all_threads
 10357-10420  _enrich_proxies_with_geo
  2139-2200   _ensure_cookie_file_netscape
  8670-8673   _ensure_notify_topic
 10601-10638  _ensure_proxy_ready
  8624-8651   _ensure_topic
   725-727    _env_int
   730-732    _env_int_range
 17143-17156  _event_webhook
 12476-12489  _evolution_loop
  5852-5886   _extract_file_payload
  2272-2274   _extract_urls_from_streamurl_node
 19972-19979  _f2b_sudo_hint
 24643-24706  _fatal_vom_botteil
 23562-23577  _fd_grenze_anheben
  4696-4706   _fehler_text
 10258-10276  _fetch_proxy_list
 17696-17724  _fetch_tiktok_room_id
   808-811    _ff_cmd
 13255-13260  _find_chromium
  3434-3436   _find_external_recorder
  2277-2279   _find_stream_urls
 12176-12201  _fire_webhooks
  7636-7645   _fork_safe
   909-922    _freeai_chat_sync_metered
 20018-20022  _geo_lookup_ips
  3700-3709   _get_ai_session
  7469-7509   _get_live_info
  2901-2908   _get_resolve_semaphore
  7918-8308   _handle_single_tracking
 23714-23716  _hb
 23719-23736  _hb_while
 12732-12734  _highlight_cfg
 12737-12766  _highlight_observe
 13263-13281  _htmlov_screenshot_cmd
 17402-17412  _httpx_proxy
 12209-12221  _in_quiet_hours
 24493-24504  _init_db_oder_abbruch
 25288-25319  _install_fast_eventloop
  9482-9536   _install_fast_json
 11808-11824  _install_faulthandler
 18642-18651  _intel_ensure_schema
 18694-18729  _intel_index_loop
 18663-18678  _intel_index_one
 18654-18660  _intel_semantic
  5221-5230   _is_authorized
  7819-7825   _is_dead
  2262-2264   _is_hevc
 20007-20009  _is_private_ip
  1779-1786   _is_process_running
  6440-6447   _is_quiet_hours
  1354-1363   _is_upload_window
  4561-4576   _iso
  9571-9584   _json_error_handler
  6662-6663   _kick_broadcaster_id
  6574-6616   _kick_follower_count
  6558-6561   _kick_slug
 11258-11265  _kick_user_token
 24481-24490  _kickmod_boot
  4151-4154   _kind_from_filename
 12238-12240  _latest_popularity
  1716-1725   _laufstand
 24075-24109  _laufstand_loop
 23653-23684  _leistung_erheben
 18305-18354  _live_react_loop
 17982-18294  _live_react_worker
  3284-3396   _live_status_aufloesen
 16544-16555  _live_transcript_push
 18296-18303  _live_users
 16994-17038  _living_title_loop
 20747-20819  _local_backup_scan
  9553-9567   _log_5xx
 23687-23711  _log_schleuse_pruefen
   798-805    _log_sicher
 13850-13862  _looks_like_codec_err
 13845-13847  _looks_like_source_expired
  7686-7716   _loop_fehler
 11828-11837  _loop_heartbeat
 23468-23501  _loop_lag_monitor
 23515-23535  _loop_stockung_melden
 23538-23548  _loop_takt_starten
 11840-11908  _loop_watchdog_thread
 16424-16438  _loyalty_add
 16415-16421  _loyalty_get
 16441-16449  _loyalty_top
 12348-12350  _manual_donations_total
  4903-4922   _manual_status
  7827-7828   _mark_dead
 10877-10893  _marketing_loop
 22039-22057  _maybe_handle_command
 24211-24235  _maybe_hype_clip
 21124-21152  _meme_klassifizieren
  4029-4052   _migrate_columns
 22318-22329  _mod_is_exempt
 22332-22337  _mod_warn_first
 22340-22343  _mod_warn_text
 12516-12524  _modlog
  1054-1056   _multistream_targets
  3076-3112   _nachschlag_ytdlp
  7648-7649   _nc_create_subprocess_exec
  7652-7653   _nc_create_subprocess_shell
 11195-11212  _news_loop
 12543-12545  _normalize_ingest
  2494-2511   _note_check_duration
  8664-8667   _notify_topic_name
  3115-3135   _ohne_url_melden
 16570-16578  _oracle_memories
 16844-16878  _oracle_memorize
 16581-16594  _oracle_persona
 16563-16567  _oracle_recent_text
 12889-12890  _ov_atomic_write
 12880-12882  _ov_bar
 15583-15595  _ov_clip_text
 12885-12886  _ov_oneline
 19684-19713  _overlay_push
 13209-13252  _overlay_render_size
 12612-12616  _overlay_session_reset
 19649-19651  _overlay_src_ok
 15667-15677  _own_invites
 13204-13206  _parse_size
 20193-20273  _parse_ssh_attacks
  7071-7104   _pause_resume_cmd
  2021-2065   _persist_refreshed_cookies
  1924-1956   _pick_checked_pull_proxy
  9655-9668   _pin_auth_value
  9714-9715   _pin_clear_fail
  9694-9697   _pin_locked
  9700-9711   _pin_note_fail
  9671-9691   _pin_ok
 19493-19518  _piper_pick_model
 19578-19627  _piper_say
 12138-12173  _post_json_threaded
 13183-13201  _probe_video_size
  1807-1824   _proc_is_recorder
 10570-10598  _proxy_pool_refresh_loop
  1890-1921   _proxy_report_recording
 23597-23608  _pruefung_verworfen
 11793-11795  _prune_stall_dumps
 10947-11117  _public_stats
  2087-2093   _pull_proxy_still
 17114-17140  _push_notify
  9874-9876   _pwa_dir
 10327-10342  _quick_validate_proxy
 12204-12206  _quiet_hours_config
  9839-9872   _rate_guard
 16385-16391  _react_warn
  7556-7595   _reap_proc
  8898-8965   _rec_auto_abschalten
  8845-8895   _rec_frueh_getrennt
  8728-8790   _rec_kategorie_melden
  8793-8842   _rec_totstreak_fortschreiben
  2534-2556   _record_check_outcome
   793-795    _redact_stream_urls
 10497-10567  _refresh_proxy_pool
  2311-2402   _resolve_via_html
  2681-2878   _resolve_via_webcast_api_v2
  2941-3024   _resolve_via_ytdlp
 21648-21777  _resolve_youtube_ingest
  2288-2308   _resolver_stumm
 12595-12606  _restream_active_sources
 13532-13656  _restream_avatar_feeder_start
 13659-13668  _restream_avatar_feeder_stop
 17755-17873  _restream_chat_guardian
 12769-12841  _restream_chat_push
 12866-12875  _restream_chat_push_async
 13284-13393  _restream_html_overlay_start
 13396-13409  _restream_html_overlay_stop
 12554-12577  _restream_overlay_files
 18358-18390  _restream_platform_state
 18558-18593  _restream_resume_after_restart
 13716-13788  _restream_tts_enqueue_wav
 13145-13177  _restream_tts_feeder
 13142-13143  _restream_tts_fifo_path
 13671-13698  _restream_tts_start
 13700-13714  _restream_tts_stop
 18396-18555  _restream_verify_loop
 20712-20724  _retention_loop
 20706-20709  _retention_scan
  2638-2640   _room_is_abo
  5890-6007   _run_ai_call
 11931-11944  _run_async_from_flask
 20012-20015  _run_priv
 25276-25284  _run_selfcheck_and_exit
 20727-20738  _s3_client
  7854-7905   _safe_send
  4829-4845   _sample_net_throughput
  2586-2613   _schedule_next_check
 20660-20703  _scheduler_loop
  4055-4059   _schema_pk
 11948-11953  _scraper_session
 22346-22385  _screen_full
 11309-11346  _sec_headers
  2267-2269   _select_stream_from_data_section
 24996-25273  _selfcheck
  8676-8710   _send_live_notice
  1377-1381   _should_defer_upload
 21198-21234  _shrink_for_discord
  9879-9891   _sicheres_ziel
 20540-20578  _sicherheits_erinnerung_loop
 24132-24149  _sign_health_check
 24152-24171  _sign_health_loop
  4579-4604   _sitzung_bestimmen
  7665-7676   _spawn
 25701-25731  _spawn_from_flask
 23611-23617  _speicher_maps
 23620-23635  _speicher_pflegen
 17414-17693  _start_chat_listener
 23580-23594  _start_gesperrt
 11911-11928  _start_loop_watchdog
 11144-11190  _stats_loop
 11123-11126  _stats_output_path
 11129-11141  _stats_write
 19530-19544  _stimme_saubern
 19551-19575  _stimme_schon_gesagt
  8387-8403   _storage_cleanup_loop
 24191-24198  _story_for
  3459-3465   _stream_url_expiry
  3467-3472   _stream_url_ttl
 15630-15637  _streamer_persona_get
 20844-20966  _system_backup
 20975-21005  _system_backup_loop
 11753-11771  _task_auf_bot_schleife
 23159-23175  _telegram_befehlsmenue
  7719-7765   _telegram_polling_fehler
 10279-10318  _test_proxy
 10825-10841  _testpush_resolve_live
  7830-7851   _tg_sprache_setzen
  8583-8593   _tg_topics_load_into_mem
  8580-8581   _tg_topics_path
  8595-8602   _tg_topics_save
  9629-9637   _token_ok
  8605-8609   _topic_forget
 12224-12235  _tracking_max_duration
  4359-4373   _tracking_remove_cleanup
  4390-4402   _tracking_resume_cleanup
  1619-1642   _try_attach_file_handler
 19520-19528  _tts_cleanup
 10801-10805  _tunnel_effective
 23944-23964  _tunnel_lage
 24020-24072  _tunnel_wacht_loop
 19016-19069  _twitch_channel_status
 22388-22533  _twitch_chat_loop
 21490-21503  _twitch_clip_versuchen
 22202-22305  _twitch_eventsub_loop
  1400-1413   _upload_queue_add
  1424-1426   _upload_queue_count
  1383-1392   _upload_queue_load
  1373-1375   _upload_queue_path
  1415-1422   _upload_queue_remove
  1394-1398   _upload_queue_save
  1428-1469   _upload_window_loop
  7529-7536   _uptime_s
 12531-12540  _url_host
  3138-3232   _url_nachschlag
   869-873    _usage_record_claude
 24305-24327  _v37_pause_source
 24269-24279  _v37_restream_restart
 24282-24302  _v37_unpause_source
  7768-7812   _verbindung_verloren
  6619-6650   _viewer_sample_loop
  9718-9721   _wants_html
  7539-7553   _warn_empty_env
 23757-23878  _watchdog_loop
 21923-21931  _wchat_thank_ok
 17182-17212  _whisper_get_model
  7626-7633   _whisper_native_section
 16372-16378  _whisper_pool
 17306-17338  _whisper_segments
 17214-17230  _whisper_stumm
 17233-17303  _whisper_transcribe
 12937-13099  _write_restream_overlay
 12899-12934  _write_restream_overlay_async
 22557-22653  _youtube_api_chat_loop
 19072-19175  _youtube_api_status
 19178-19245  _youtube_channel_status
 22656-22817  _youtube_chat_loop
 21506-21531  _youtube_clip_versuchen
 21783-21796  _youtube_restream_autoconfig
 21799-21823  _youtube_restream_autoconfig_inner
 21890-21918  _youtube_send
 19313-19354  _youtube_set_channel
 21826-21860  _yt_access_token
 21863-21878  _yt_live_chat_id
 21886-21887  _yt_sendrate_cfg
 22536-22551  _yt_timeout
  2925-2926   _ytdlp_detect_available
  2928-2939   _ytdlp_note_result
 11798-11800  _zombie_child_count
  7405-7429   about
  4270-4274   add_ai_log_entry
  4187-4190   add_archive_entry
  4867-4869   add_archive_rule
  4607-4678   add_recording
  4334-4351   add_tracking
  6010-6043   ai
  3852-3933   ai_chat
  3967-3977   ai_history_append
  3979-3984   ai_history_clear
  3956-3965   ai_history_load
  3941-3954   ai_rate_limit_check
  6072-6080   aireset
 16711-16730  azrael_chat
 22822-22944  brain_cmd
  3475-3480   build_recording_cmd
  4354-4357   bulk_add_trackings
  6873-6932   bulkadd
  8406-8563   check_all_trackings
  4406-4418   claim_live_transition
 15707-16304  class KickModerator
 13865-15470  class RestreamManager
 10684-10726  classify_proxy_anonymity
  6118-6316   cleanup
  5157-5163   cleanup_old_recordings
  4552-4559   clear_recording
 21534-21605  clip_moment
  4819-4822   compute_storage_forecast
  6995-7068   cookies_cmd
  4325-4331   count_trackings_for_chat
  4257-4268   decide_preferred_recorder
  4197-4200   delete_archive_entry
  4871-4873   delete_archive_rule
  5547-5694   diag
 23056-23117  einnahmen_cmd
  4813-4816   find_recordings_by_fingerprint
  4218-4234   finish_recording_attempt
  4378-4380   get_all_active_trackings
  4285-4287   get_all_checks
  4680-4683   get_all_recordings
  4762-4764   get_all_tags_with_counts
  4790-4793   get_annotations_for_recording
  4192-4195   get_archive_entry
  4783-4786   get_bookmarked_recordings
  2127-2132   get_cookie_health
  4750-4756   get_event_log
  4241-4255   get_last_recording_attempt
  3235-3277   get_live_status
  5096-5099   get_manual_recordings
  4798-4801   get_or_compute_inspect_sync
  5198-5201   get_outcome_breakdown
  4769-4772   get_priority_poll_interval
  4236-4239   get_recent_recording_attempts
  4685-4688   get_recording_by_id
  4776-4779   get_recording_note
  3646-3669   get_redis
  4314-4317   get_stats
  5151-5155   get_storage_stats
  4891-4893   get_tiktok_status_distribution
  4420-4429   get_tracking_state
  4375-4376   get_trackings_for_group
  5112-5115   get_trash_recordings
  9004-9461   handle_recording_finished
 23151-23156  hilfe_cmd
  4082-4142   init_db
  4863-4865   list_archive_rules
  5351-5389   live
  7908-7916   live_check_worker
  3724-3763   llm_chat
  3786-3816   llm_chat_sync
  3771-3783   llm_list_models
  4709-4742   log_event
  1741-1774   log_recording_failure
  7218-7267   logs_cmd
 24709-24986  main
  6046-6069   on_ai_media
  7344-7370   on_ai_reply
  7373-7402   on_azrael_mention
  7434-7464   on_callback
 16736-16841  oracle_handle
  7107-7110   pause_tracking
  5211-5216   profile_keyboard
  7169-7215   quota
  8310-8384   reaper_loop
  4887-4889   record_tiktok_status
  6085-6115   recstatus
  3671-3679   redis_get_json
  3682-3688   redis_set_json
 23178-23188  report_cmd
 10729-10731  report_proxy_result
  2405-2447   resolve_tiktok_live_stream
  5107-5110   restore_recording
  7113-7116   resume_tracking
  4876-4881   run_archive_rules
 23191-23448  run_bot
 11650-11744  run_flask
  4851-4854   sample_bandwidth_for_active
  4277-4283   save_tiktok_check
  4544-4550   set_recording_file
  4383-4387   set_tracking_paused
  5102-5105   soft_delete_recording
  8716-8726   split_and_send_video
  5264-5306   start
  4202-4216   start_recording_attempt
  6319-6357   stats
  5041-5094   stop_manual_recording
  7119-7166   stoprec
  6543-6551   summary_cmd
  7270-7341   sysres
  5696-5840   teststream
  5308-5349   tiktok
  6935-6992   topusers
  5426-5483   track
  5391-5423   track_exact
  5497-5545   tracklist
  4925-5039   trigger_manual_recording
  4505-4542   try_acquire_recording_lock
  5118-5120   universal_search
 23120-23148  unpause_cmd
  5485-5495   untrack
 22947-23053  update_cmd
  4808-4811   update_recording_fingerprint
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
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
betriebslage.py        bereit, bewerten, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
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
kennzahlen.py          prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, entkoppeln, nachziehen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
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
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, schriftart
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
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
telegramfehler.py      dauer_text, grund, ist_fehler, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
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
